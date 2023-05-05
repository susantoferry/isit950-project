from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from backend.models import *
from .constant import *
from urllib.parse import urlencode
from django.conf import settings
import requests
import re
from urllib.parse import urlparse
import hashlib

# Create your views here.
@login_required
def index(request):
    return redirect("tasks")

def profile(request):
    return render(request, "isit950/account/profile/dashboard-profile.html")

def createProfile(request):
    return render(request, "isit950/account/profile/create_profile.html")

def editProfile(request):
    if request.method == 'GET':
        profileResp = requests.get(restServer + "profile_api/" + request.user.username)
        skillsResp = requests.get(restServer + "my_skilllist/" + request.user.username)
        if profileResp.status_code == 200 and skillsResp.status_code == 200:
            profile = profileResp.json()
            skills = skillsResp.json()
            
            return render(request, "isit950/account/profile/edit_profile.html", {
                "profile": profile,
                "skills": skills
            })
        else:
            return render(request, "isit950/404.html")

    if request.method == 'POST':
        profileData = {
            'description': request.POST["description"],
            'address': request.POST["address-search"],
            'unit': request.POST["unit"],
            'city': request.POST["city"],
            'state': request.POST["state"],
            'zip': request.POST["zip"]
        }

        profileResp = requests.put(f"{restServer}profile_api/{request.user.username}", json=profileData)

        if profileResp.status_code == 200:
            messages.success(request, "Profile has been updated successfully")
            return HttpResponseRedirect(reverse("edit_profile"))
        else:
            messages.error(request, "There is an error when updating")
            return HttpResponseRedirect(reverse("edit_profile"))

def tasks(request):
    taskResp = requests.get(restServer + "task")
    tasks = taskResp.json()
    
    # firstTaskDetail = tasks[0]["id"]
    # taskDetailResp = requests.get(restServer + 'task/' + str(firstTaskDetail))
    # taskDetail = taskDetailResp.json()

    # commentResp = requests.get(f"{restServer}question/{firstTaskDetail}")
    # comments = commentResp.json()
    
    # parentQuestion = Question.objects.filter(task_id=firstTaskDetail, parent_id=None).order_by("-create_date")
    # childQuestion = Question.objects.filter(task_id=firstTaskDetail).exclude(parent_id=None)
    
    response =  render(request, "isit950/index.html", {
        "tasks": tasks,
        # "taskDetail": taskDetail,
        "user": request.user,
        # "comments": comments,
        # "parentQuestion": parentQuestion,
        # "childQuestion": childQuestion
    })
    
    if request.user.is_authenticated and not request.COOKIES.get('usid'):
        response.set_cookie(key='usid', value=request.user.username, max_age=settings.SESSION_COOKIE_AGE)
        
    return response

def taskDetail(request, slug):
    
    taskId = slug.rsplit('-', 1)[-1]
    
    taskResp = requests.get(restServer + "task")
    tasks = taskResp.json()
    
    taskDetailResp = requests.get(restServer + 'task/' + str(taskId))
    taskDetail = taskDetailResp.json()

    parentQuestion = Question.objects.filter(task_id=taskId, parent_id=None).order_by("-create_date")
    childQuestion = Question.objects.filter(task_id=taskId).exclude(parent_id=None)

    # return JsonResponse({
    #     "taskDetail": taskDetail
    # })

    return render(request, "isit950/index.html", {
        "tasks": tasks,
        "taskDetail": taskDetail,
        "parentQuestion": parentQuestion,
        "childQuestion": childQuestion
    })

def searchTask(request):
    params = {
                'search_keyword': request.GET.get('search_keyword', None),
                'category': request.GET.getlist('category', None), 
                'min_price': request.GET.get('min_price', 0),
                'max_price': request.GET.get('max_price', 9999),
                'location': request.GET.get('location', None),
                'sort_type': request.GET.get('sort_type', None)      
            }
    
    searchTaskResp = requests.get(restServer + "search_task", params=params)
    searchTask = searchTaskResp.json()

    return render(request, "isit950/index.html", {
        "tasks": searchTask    
    })

def createTask(request):
    if request.method == 'GET':
        # print(decryptString(request.COOKIES.get('usid')))
        
        catResp = requests.get(restServer + "category")
        categories = catResp.json()

        return render(request, "isit950/create_task.html", {
            "categories": categories    
        })


    if request.method == 'POST':
        task = Task(
            task_title = request.POST["task_title"].lstrip(),
            category_id = request.POST["category"].lstrip(),
            description = request.POST["task_description"],
            price = request.POST["price"],
            location = request.POST["location"].lstrip(),
            location_link = request.POST["location_url"].lstrip(),
            completed_on = request.POST["completed_on"].lstrip(),
            user_id = 1
        )
        task.save()
        # task = {
        #     "task_title" : request.POST["task_title"].lstrip(),
        #     "category" : request.POST["category"].lstrip(),
        #     "description" : request.POST["task_description"],
        #     "price" : request.POST["price"],
        #     "location" : request.POST["location"].lstrip(),
        #     "location_link" : request.POST["location_url"].lstrip(),
        #     "completed_on" : request.POST["completed_on"].lstrip(),
        #     "user": 1
        # }
        # requests.post(restServer, data=task)

        
        messages.success(request, "New task has been added successfully")
        return HttpResponseRedirect(reverse("tasks"))
    
def notification(request):
    return render(request, "isit950/account/notification.html")

def paymentMethod(request):
    return render(request, "isit950/account/payment_method.html")

def paymentHistory(request):
    return render(request, "isit950/account/payment_history.html")
    
def testRead(request):
    if request.method == 'POST':
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        name = request.POST['text-content']
        for i in name.split():
            i = i.lstrip()
            if(re.fullmatch(regex, i)) or (re.fullmatch('[6-9][0-9]{9}',i)):
                print("contain number")
        
            else:
                print("no number")



        return HttpResponseRedirect(reverse("test123"))

    return render(request, "isit950/index.html")

def watchlist(request):
    watchlistResp = requests.get(restServer + "show_my_watchlist/ferry")
    watchlist = watchlistResp.json()

    return render(request, "isit950/watchlist.html", {
        "watchlist": watchlist
    })

def wishlist(request):
    wishistResp = requests.get(restServer + "show_my_watchlist/ferry")
    wishlist = wishistResp.json()

    return render(request, "isit950/account/wishlist.html", {
        "wishlist": wishlist
    })

def myTask(request):
    userId = str(request.user.id)
    myTaskListResp = requests.get(restServer + "get_my_task/" + userId)
    myTaskList = myTaskListResp.json()
    
    firstTaskDetail = myTaskList[0]["id"]
    taskDetailResp = requests.get(restServer + 'task/' + str(firstTaskDetail))
    taskDetail = taskDetailResp.json()
    
    return render(request, "isit950/my_task.html", {
        "myTaskList": myTaskList,
        "taskDetail": taskDetail,
        "type": "myTask"
    })

def myTaskDetail(request, taskId):
    myTaskDetailResp = requests.get(restServer + "task/" + str(taskId))
    myTaskDetail = myTaskDetailResp.json()

    offerResp = requests.get(restServer + "offer/" + str(taskId))
    offers = offerResp.json()

    questionCount = Question.objects.filter(task=taskId, parent_id__isnull=True).count()

    return render(request, "isit950/my_task_detail.html", {
        "myTaskDetail": myTaskDetail,
        "offers": offers,
        "questions": questionCount
    })

def resendEmail(request, email):

    resendResp = requests.post(restServer + 'resend_email_api', json={'email': email})

    return HttpResponseRedirect(reverse("verify_email", args=[email]))

def verifyEmail(request, email):
    
    return render(request, "isit950/auth/verify_account.html", {
        "email": decryptString(email),
        "code": email
    })

def verifyingEmail(request, email):
    verifyResp = requests.post(restServer + 'verifying-email-api', json={'email': email})

    if verifyResp.status_code == 200:
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse("verify_email", args=[email]))

def postTask(request):
    return render(request, "isit950/postTask.html")

def test2HTML(request):
    return render(request, "isit950/test2.html")

def test3HTML(request):
    return render(request, "isit950/test3.html")

def loginView1(request):
    return render(request, "isit950/auth/login1.html")

def loginView(request):
    
    if request.method == 'GET':
        
        return render(request, "isit950/auth/login.html")
    
    if request.method == 'POST':
        userData = {
            'email': request.POST["email"],
            'password': request.POST["password"]
        }
        
        userRequest = requests.post(restServer + "user_login" , json=userData)

        if userRequest.status_code == 200:
            username = userRequest.json()['user']
            user = authenticate(request, username=username, password=request.POST["password"])

            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "isit950/auth/login.html", {
                "message": "Invalid username and/or password.",
                "status": "danger"
            })
        
def registerView(request):
    if request.method == 'GET':
        return render(request, "isit950/auth/register.html")

    if request.method == 'POST':

        if request.POST["password"] != request.POST["confirmPassword"]:
            return render(request, "isit950/auth/register.html")
        else:
            userData = {
                'first_name': request.POST["firstName"],
                'last_name': request.POST["lastName"],
                'email': request.POST["email"],
                'password': request.POST["password"]
            }

            # return HttpResponseRedirect(reverse("verify_email", args=[encryptString(request.POST["email"])]))

            registerRequest = requests.post(restServer + "register_api" , json=userData)

            if registerRequest.status_code == 200:
               return HttpResponseRedirect(reverse("verify_email", args=[encryptString(request.POST["email"])]))
            else:
                return render(request, "isit950/auth/register.html")

def forgotPass(request):
    if request.method == "POST":
        data = {
            'email': request.POST["email"],
        }

        forgotPass = requests.post(restServer + "forgot_password_api", json=data)

        if forgotPass.status_code == 200:
            return render(request, "isit950/auth/forgot_password.html", {
                "submit": True
            })
        else:
            return render(request, "isit950/auth/forgot_password.html", {
                "message": "Invalid username and/or password.",
                "status": "danger"
            })
    else:

        return render(request, "isit950/auth/forgot_password.html")

def resetPass(request, token):
    if request.method == 'POST':
        data = {
            'password': request.POST["password"],
            'password2': request.POST["confPassword"]
        }
        
        resetPassRequest = requests.post(f"{restServer}reset_password_api/{token}", json=data)
        if resetPassRequest.status_code == 200:
            return HttpResponseRedirect(reverse("index"))
        else:

            # Construct the redirect URL with args and redirect the user
            # return HttpResponseRedirect(reverse("reset_password", args=[token]))
            error = "Password cannot be common and must match"

            return render(request, "isit950/auth/reset_password.html",{
                "token": token,
                "error": error
            })

    if request.method == 'GET':
        # check token status and datetime
        checkToken = requests.get(f"{restServer}reset_password_api/{token}")

        # if token is been used or expired
        if checkToken.status_code == 200:

            return render(request, "isit950/auth/reset_password.html",{
                "token": token
            })
        else:
            return render(request, "isit950/auth/reset_password.html", {
                "expired": True
            })

def logout_view(request):
    logout(request)
    # return HttpResponseRedirect(reverse("index"))

    response = HttpResponseRedirect(reverse("index"))
    response.delete_cookie('usid')
    return response

# def selectTasker(request, taskId, userId):
#     Task.objects.filter(pk=taskId).update(status=1, user_provider=userId)

#     return redirect('my_task', taskId)

# def login_view(request):
#     if request.method == "POST":
#         # case insensitive username to login
#         username = User.objects.values_list('username', flat=True).get(username__icontains=request.POST["username"].lower())
#         # Attempt to sign user in
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)

#         # Check if authentication successful
#         if user is not None:
#             # request.session['fav_color'] = 'blue'
#             # <li>{{ request.session.fav_color }}</li>
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             return render(request, "admin_piano/account/login.html", {
#                 "message": "Invalid username and/or password.",
#                 "status": "danger"
#             })
#     else:
#         return render(request, "admin_piano/account/login.html")

# def logoutV(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))