from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from backend.models import *
from .constant import *

import requests
import re


# Create your views here.

def index(request):
    return redirect("tasks")

def profile(request):
    return render(request, "isit950/account/profile.html")

def tasks(request):
    taskResp = requests.get(restServer + "task")
    tasks = taskResp.json()
    
    firstTaskDetail = tasks[0]["id"]
    taskDetailResp = requests.get(restServer + 'task/' + str(firstTaskDetail))
    # taskDetail = taskDetailResp.json()

    commentResp = requests.get(f"{restServer}question/{firstTaskDetail}")
    comments = commentResp.json()
    
    parentQuestion = Question.objects.filter(task_id=firstTaskDetail, parent_id=None).order_by("-create_date")
    childQuestion = Question.objects.filter(task_id=firstTaskDetail).exclude(parent_id=None)

    return render(request, "isit950/index.html", {
        "tasks": tasks,
        "taskDetail": taskDetail,
        "user": 1,
        "comments": comments,
        "parentQuestion": parentQuestion,
        "childQuestion": childQuestion
    })

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

def createTask(request):
    if request.method == 'GET':
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
    
def membershipPlan(request):
    return render(request, "isit950/account/membership_plan.html")

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