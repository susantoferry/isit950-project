from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
from .constant import *

# Create your views here.
def index(request):
    taskResp = requests.get(restServer + "task")
    tasks = taskResp.json()
    
    firstTaskDetail = tasks[0]["id"]
    taskDetailResp = requests.get(restServer + 'task/' + str(firstTaskDetail))
    taskDetail = taskDetailResp.json()

    # watchlistResp = requests.get(restServer + "watchlist/ferry")
    # watchlist = watchlistResp.json()
    # for i in watchlist:
    #     print(i["tasks"]["task_title"])
    
    return render(request, "isit950/index.html", {
        "tasks": tasks,
        "taskDetail": taskDetail,
        # "watchlist": watchlist
    })

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