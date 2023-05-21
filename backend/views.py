from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models import Q
from datetime import datetime, timedelta

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from backend.models import *
from knox.auth import AuthToken
from .serializers import *

from random import randint

from frontend.constant import *

from PIL import Image 

import os
import time
import uuid
import random
import string
import base64
import json

from io import BytesIO
from asgiref.sync import sync_to_async

# Create your views here.

@api_view(['GET', 'POST'])
def index(request):
    # category = Category.objects.raw('SELECT * FROM')
    category = Category.objects.raw("SELECT * FROM backend_category")
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

def make_thumbnail(image, size, fldr):
    """Makes thumbnails of given size from given image"""
    if image != "":
        im = Image.open(image)
        # im = im.convert('RGB')
        # Transparent background
        if im.mode != "RGBA":
            im = im.convert("RGBA")
            
        timestr = time.strftime("%y%m%d%H%M%S")
        # if fldr != "home":
        #     im.thumbnail(size) # resize image
        # ext = image.name.split('.')[-1]
        file_name = '{}.{}'.format(uuid.uuid4().hex[:15] + timestr, "png")

        # file path relative to 'media' folder
        absolute_file_path = os.path.join('frontend/static/images/', fldr, file_name)
        file_loc = 'images/' + fldr + '/' + file_name

        directory = os.path.dirname(absolute_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        im.save(absolute_file_path, quality=75)
    # return os.path.join('images/profiles', file_name)
    return file_loc

def delete_image(img_name):
    if img_name != "":
        os.remove("./frontend/static/" + img_name, dir_fd=None)

@api_view(['GET', 'POST'])
def category(request):
    if request.method == 'GET':
        category = Category.objects.raw("SELECT * FROM backend_category")
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def categoryDetail(request, id):
    if request.method == 'GET':
        category = Category.objects.raw("SELECT * FROM backend_category WHERE id = %s", [id])
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        
        serializer = CategorySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
def userProfile(request, user):
    try:
        profile = User.objects.get(username=user)
    except User.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        if profile:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=200)
        else:
            return Response(status=400)

    if request.method == 'PUT':
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response(status=404)
        
        saveUser = {}
        if user != "":
            for i in request.data:
                if i == 'img_profile':
                    saveUser.update({i: make_thumbnail(request.FILES[i], "", 'profiles')})
                    # delete_image(request.FILES[i])
                elif i == 'img_background':
                    saveUser.update({i: make_thumbnail(request.FILES[i], "", 'profiles_bg')})
                    # delete_image(request.FILES[i])
                else:
                    saveUser.update({i: request.data[i]})

            serializer = ProfileSerializer(user, data=saveUser)
            if serializer.is_valid():
                serializer.save()
                return Response("User has been successfully updated")
            else:
                return Response(serializer.errors)
        else:
            return Response("not found")
        
@api_view(['GET'])
def getAllQuestion(request, taskId, parent='no'):
    print(parent)
    print(taskId)
    if parent == "yes":
        questions = Question.objects.filter(task_id=taskId).exclude(parent_id=None)
    else:
        questions = Question.objects.filter(task_id=taskId, parent_id=None).order_by("-create_date")
    print(questions)
    serializer = QuestionSerializer(questions, many=True)

    return Response(serializer.data)

    
@api_view(['POST'])
def question(request, taskId):
    if request.method == 'POST':
        request.data['user'] = User.objects.values_list('id', flat=True).get(username=request.data['user'])
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def offer(request):
    if request.method == 'GET':
        offers = Offer.objects.all().order_by("-modify_date")
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        request.data["task"] = request.data["task"].rsplit('-', 1)[-1]
        
        request.data['user'] = User.objects.values_list('id', flat=True).get(username=request.data['user'])
        print(request.data)

        serializer = OfferSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "message": "Saved successfully"})
        else:
            return Response(serializer.errors,status=400)
        

@api_view(['GET'])
def offerDetail(request, taskId):
    taskId = taskId.rsplit('-', 1)[-1]
    offers = Offer.objects.filter(task_id = taskId)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)
        
@api_view(['GET', 'PUT', 'DELETE'])
def offerDetail1(request, taskId):
    try:
        task = Task.objects.get(id=taskId)
    except Task.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=404)
   
    
@api_view(['GET'])
def notification(request, user):
    if request.method == 'GET':
        notifications = Notification.objects.filter(user=user).order_by('-create_date')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def updateNotifStatus(request, notifId, user):
    if request.method == 'POST':
        try:
            getNotif = Notification.objects.get(pk=notifId, user=user)
        except Notification.DoesNotExist:
            getNotif = ""

        if getNotif:
            data = JSONParser().parse(request)
            if getNotif.is_read == data['is_read']:
                return Response("Nothing changes", status=200)
            else:
                serializer = ReadNotificationSerializer(getNotif, data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(status=200)
                else:
                    print(serializer.errors)
                    return Response(status=404)
        else:
            print("aaa")
            return Response("Data cannot be found",status=404)

        
@api_view(['GET'])
@csrf_protect
def getMyTask(request, userId):
    myTasks = Task.objects.filter(user_id=userId).order_by("status","-create_date")
    serializer = TaskSerializer(myTasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def acceptOffer(request, taskId, userSpId):
    try:
        task = Task.objects.get(pk=taskId)
    except Task.DoesNotExist:
        task = ""
    
    if task != "":
        if request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = TaskSerializer(task, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                print(serializer.errors)
                return Response(status=404)

    else:
        return Response("Error")

@api_view(['GET', 'POST'])
def task(request):
    if request.method == 'GET':
        tasks = Task.objects.all().order_by("status","-modify_date")
        # tasks = Task.objects.raw('select t.*, p.first_name, p.last_name, p.rating, p.img_profile from backend_task t join backend_profile p on t.user_id = p.user_profile_id ORDER BY t.status, t.modify_date DESC')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            sendTaskNotification(instance.id, request.data["content"], request.data["location"], request.data["user"], "")
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def taskDetail(request, taskId):

    taskId = taskId.rsplit('-', 1)[-1]

    if request.method == 'GET':
        try:
            task = Task.objects.get(id=taskId)
        except Task.DoesNotExist:
            return Response(status=404)
        
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        
        try:
            task = Task.objects.get(id=taskId, user=data["user"])
        except Task.DoesNotExist:
            return Response("You are not authorise to edit this task",status=404)

        serializer = TaskSerializer(task, data=data)
        
        if serializer.is_valid():
            serializer.save()
            sendTaskNotification(taskId, data["content"], data["location"], data["user"])
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=404)
        
@api_view(['PUT'])
def updateTaskStatus(request, taskId):
    
    taskId = taskId.rsplit('-', 1)[-1]

    if request.method == 'PUT':
        is_provider = ""
        data = JSONParser().parse(request)
        
        try:
            task = Task.objects.get(id=taskId, user=data["user"])
        except Task.DoesNotExist:
            return Response("You are not authorise to edit this task", status=404)
        
        serializer = UpdateTaskStatusSerializer(task, data=data)
        
        if serializer.is_valid():
            serializer.save()
            if "user_provider" in data:
                is_provider = data["user_provider"]    
            
            sendTaskNotification(taskId, data["content"], task.location, data["user"], is_provider)
            
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=404)
        
def sendTaskNotification(taskId, content, location, clientId, userProvider):
   
    if content < 5:
        # Get all users who have membership as SP or Full Package
        userMemberships = MembershipTransaction.objects.filter(user__address=location, membership__in= [1,3]).exclude(user=clientId)
        
        for member in userMemberships:
            
            notification = {
                'content_notif': content,
                'task': taskId,
                'user': member.user.id
            }
            serializer = NotificationSerializer(data=notification)
            
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)
    else:
        if content > 5:
            user = [clientId, userProvider]
            for u in range(len(user)):
                notification = {
                    'content_notif': content,
                    'task': taskId,
                    'user': user[u]
                }
                
                serializer = NotificationSerializer(data=notification)
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors)
        else:
            notification = {
                'content_notif': content,
                'task': taskId,
                'user': userProvider
            }
            serializer = NotificationSerializer(data=notification)
            
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

    return Response("success", status=200)

@api_view(['GET'])
def sendTaskNotification1(request, taskId, content, location, clientId):
    # Get all users who have membership as SP or Full Package
    userMemberships = MembershipTransaction.objects.filter(user__address=location, membership__in= [1,3]).exclude(user=clientId)
    
    for member in userMemberships:
        notification = {
            'content_notif': content,
            'task': taskId,
            'user': member.user.id
        }

        serializer = NotificationSerializer(data=notification)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

    return Response("a")
        
@api_view(['GET','POST'])
def membershipTransaction(request):
    if request.method == 'POST':

        price = {
            '1': 80,
            '2': 50,
            '3': 120
        }

        try:
            membership = MembershipTransaction.objects.filter(user = request.data['user']).order_by("-create_date").first()
        except MembershipTransaction.DoesNotExist:
            membership = ""
        
        # Check if user has membership
        if membership:
            # if the current membership is same with request data then return response
            if request.data["membership"] == membership.membership:
                return Response("The current membership is same.", status=200)
            
            # Determine transaction type membership
            if request.data['membership'] == 0:
                request.data['trans_type'] = 'D'
                request.data["price"] = 0
            else:
                request.data['trans_type'] = 'U'
                
                # Change price if the package is either 1 or 2 change to 3
                if int(request.data["membership"]) == 3:
                    request.data["price"] = price[request.data['membership']] - membership.price
                else:
                    print(price[request.data["membership"]])
                    request.data["price"] = price[request.data["membership"]]
        else:
            request.data['trans_type'] = 'A'
            request.data["price"] = price[request.data["membership"]]
        
        if request.data['membership'] == 0:
            request.data["credit_card"] = "-"
        else:
            request.data["credit_card"] = str(encryptString(request.data['credit_card']))

        serializer = MembershipTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=404)
        
@api_view(['GET'])
def taskSearch(request):
    if request.method == 'GET':
        search_keyword = request.GET.get('search_keyword', None)
        category = request.GET.getlist('category', None)
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 9999)
        location = request.GET.get('location', None)
        sort = request.GET.get('sort_type', None)

        if search_keyword != None:
            searchTask = Task.objects.filter(task_title__icontains = search_keyword, price__gte=min_price, price__lte=max_price)
        else:
            if len(category) == 0:
                searchTask = Task.objects.filter(price__gte=min_price, price__lte=max_price, location__icontains=location)
            else:
                searchTask = Task.objects.filter(category__name__in=category, price__gte=min_price, price__lte=max_price, location__icontains=location)

        if sort is None or sort.lower() == "newest":
            searchTask = searchTask.order_by('create_date')

        if sort is not None:
            if sort.lower() == 'oldest':
                searchTask = searchTask.order_by('-create_date')
            if sort.lower() == 'lowtohigh':
                searchTask = searchTask.order_by('price')
            if sort.lower() == 'hightolow':
                searchTask = searchTask.order_by('-price')

        serializer = TaskSerializer(searchTask, many=True)
        return Response(serializer.data)
    else:
        return Response(status=400)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def taskDetail(request, taskId):
#     print(taskId)
#     try:
#         # task = Task.objects.get(id=taskId)
#         # test = Task.objects.get(id=taskId)
#         # test1 = Profile.objects.get(user_profile=test.user.id)
        
#         # sql = ("SELECT t.*, p.first_name, p.last_name, p.rating, p.img_profile FROM backend_task t"
#         #       'JOIN backend_profile p ON t.user_id = p.user_profile_id WHERE t.id = %s'
#         #       'ORDER BY t.status, t.modify_date DESC', [taskId]')
#         sql = "SELECT t.*, p.first_name, p.last_name, p.rating, p.img_profile FROM backend_task t JOIN backend_profile p ON t.user_id = p.user_profile_id WHERE t.id = 22 ORDER BY t.status, t.modify_date DESC"
#         print(sql)
#         task = Task.objects.raw(sql)[0]
#         # result = {}
#         # keys = ('first_name','last_name','rating')
#         # for row in task:
        
        
#         # result['id'] = 22
#         # result['task_title'] = 'title'
#         # result['description'] = 'description'
#         # result['location'] = 'location'
#         # result['location_link'] = 'location link'
#         # result['completed_on'] = '2023-04-20'
#         # result['category'] = 'category'
#             # "task_title": "title",
#             # "first_name": "first_name",
#             # "last_name": "last_name",
#             # "rating": "rating"
        
#         # print(result)
#     except Task.DoesNotExist:
#         return Response(status=404)
    
#     if request.method == 'GET':
#         serializer = TaskSerializer(task, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(task, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=200)
#         else:
#             print(serializer.errors)
#             return Response(status=404)

@api_view(['GET'])
def priceCategory(request, category):
    if request.method == 'GET':
        priceCat = Price.objects.get(category=category)

        serializer = PriceSerializer(priceCat)
        return Response(serializer.data)
        

@api_view(['GET'])
def myWatchlist(request, user):
    if request.method == 'GET':
        # Get user id by username
        userId = User.objects.get(username=user)

        watchlist = Watchlist.objects.all().filter(user=userId.id)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def watchlist(request):
    if request.method == 'POST':
        user = request.data['user']
        task = request.data['task']

        try:
            userId = User.objects.get(username=user)
        except User.DoesNotExist:
            userId = ""
        
        if userId != "":
            try:
                watchlist = Watchlist.objects.get(task=task, user=userId.id)
            except Watchlist.DoesNotExist:
                watchlist = ""

            if watchlist == "":

                data = {
                    'task': request.data['task'],
                    'user': userId.id
                }

                serializer = WatchlistSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
            else:
                watchlist.delete()
                return Response({
                    "success"
                }, status=200)
        else:
            print("a")
            return Response("error")
        
@api_view(['GET'])
def reviewType(request, type, user):    
    if type == 'client':
        review = Review.objects.filter(user_client = user)

    if type == 'sp':
        review = Review.objects.filter(user_sp = user)

    serializer = ReviewSerializer(review, many=True)
    return Response(serializer.data)
    # return Response(serializer.errors)

@api_view(['POST'])
def review(request):
    if request.method == "POST":
        taskId = request.data['task']
        try:
            review = Review.objects.get(task=taskId)
        except Review.DoesNotExist:
            review = ""

        try:
            task = Task.objects.get(Q(pk=taskId) & (Q(provider_review=False) | Q(user_review=False)))
        except Task.DoesNotExist:
            task = ""

        if task:
            if 'user_client' in request.data:
                task.user_review = True
            else:
                task.provider_review = True

            task.save()

        if review == "":
            serializer = ReviewSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response("success", status=200)
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = ReviewSerializer(review, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response("success", status=200)
            else:
                return Response(serializer.errors, status=400)
        

@api_view(['GET', 'POST'])
def skill(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
   
@api_view(['GET', 'PUT', 'DELETE'])
def skillDetail(request, id):
    try:
        skill = Skill.objects.get(pk=id)
    except Skill.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = SkillSerializer(skill, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SkillSerializer(skill, data=data)
@api_view(['GET', 'POST'])
def skill(request):
    if request.method == 'GET':
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
   
@api_view(['GET', 'PUT', 'DELETE'])
def skillDetail(request, id):
    try:
        skill = Skill.objects.get(pk=id)
    except Skill.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = SkillSerializer(skill, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SkillSerializer(skill, data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        skill.delete()
        return Response(status=204)



@api_view(['GET', 'POST'])
def membership1(request):
    if request.method == 'GET':
        memberships = Membership.objects.all()
        serializer = MembershipSerializer(memberships, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MembershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def membershipDetail1(request, id):
    try:
        membership = Membership.objects.get(pk=id)
    except Membership.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = MembershipSerializer(membership, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MembershipSerializer(membership, data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        membership.delete()
        return Response(status=204)

@api_view(['GET','POST','DELETE'])
@csrf_exempt
def mySkillList(request,user):
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        user = ""
    if user != "":
        if request.method == 'GET':
            # user = User.objects.get(username=user)
            skilllist = UserSkill.objects.all().filter(user=user.id)
            serializer = UserSkillSerializer(skilllist, many=True)
            return Response(serializer.data, status=200)

        if request.method == 'DELETE':
            try:
                userSkill = UserSkill.objects.get(user=user.id, id=request.data['id'])
            except UserSkill.DoesNotExist:
                userSkill = ""

            if userSkill:
                userSkill.delete()
                return Response({"success"}, status=200)
            else:
                return Response(status=400)

        if request.method == "POST":
            # skill = request.data.get('skill')
            data = {
                "user": user.id,
                "skill": request.data['skill']
            }
            serializer = UserSkillSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)

    else:
        return Response("User cannot be found!")

def getUsername(user):
    result = ""
    while True:
        username = user.lower() + str(randint(100,999))
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = ""
        
        if user == "":
            result = username
            break

    return result
        
@api_view(['GET','POST'])
def userLogin(request):
    if request.method == 'GET':
        return Response("a")
    #     user = 'ferry'
    #     print(user)

    #     if user.is_authenticated:
    #         return Response({
    #             'user_info': {
    #                 'id': user.id,
    #                 'username': user.username,
    #                 'email': user.email
    #             }
    #         })
    #     return Response({'error': 'not authenticated'}, status=400)

    if request.method == "POST":
        if "email" in request.data:
            user = User.objects.values_list('username', flat=True).filter(email=request.data["email"], email_verified=1)
            if user.exists():
                request.data["username"]= user[0]
            else:
                return Response({"message", "Not found."}, status=404)
        
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = AuthToken.objects.create(user)[1]
            
            return Response({'message': 'Success', 'user': str(user)}, status=200)
        else:
            return Response(serializer.errors, status=404)
        # return Response({
        #     'user_info': {
        #         'id': user.id,
        #         'username': user.username,
        #         'email': user.email
        #     },
        #     'token': token
        # })

@api_view(['POST'])
def userRegister(request):
    username = request.data["first_name"][0:3] + request.data["last_name"][0:3]
    username = getUsername(username)
    
    try:
        email = User.objects.get(email = request.data["email"])
    except:
        email = ""
    
    if email == "":
        user = {
            'username': username,
            'first_name': request.data["first_name"],
            'last_name': request.data["last_name"],
            'email': request.data["email"],
            'password': request.data["password"]
        }

        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            serializer.save()

            html_content = render_to_string("verify_email.html", {'email': encryptString(user['email'])})
            email = EmailMessage(
                subject = 'Verify your email',
                body = html_content,
                from_email = "Ferry Susanto UOW <ferry.milanisti22@gmail.com>",
                to = [user['email']]
            )
            email.content_subtype = "html"
            time.sleep(2)
            email.send()

            return Response("success", status=200)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response("Username is not available", status=400)
    
    
    # return Response({
    #     'userDetail': {
    #         'id': user.id,
    #         'username': user.username,
    #         'email': user.email
    #     },
    #     "token": AuthToken.objects.create(user)[1]
    # }, status=200)

@api_view(['POST'])
def resendEmailAPI(request):
    
    html_content = render_to_string("verify_email.html", request.data)
    email = EmailMessage(
        subject = 'Verify your email',
        body = html_content,
        from_email = "Ferry Susanto UOW <ferry.milanisti22@gmail.com>",
        to = ["yohanesfersusanto@gmail.com"]
    )
    email.content_subtype = "html"
    time.sleep(2)
    email.send()
    return Response(status=200)

@api_view(['POST'])
def verifyingEmailAPI(request):
    try:
        user = User.objects.get(email=decryptString(request.data['email']))
    except User.DoesNotExist:
        user = ""

    if user != "":
        user.email_verified = True
        user.save()
        return Response(status=200)
    else:
        return Response({'not found'}, status=400)


@api_view(['POST'])
def ChangePassword(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=404)
    

    serializer = ChangePasswordSerializer(data=request.data)
    if not user.check_password(request.data["old_password"]):
        raise serializers.ValidationError({"old_password": "Old password is not correct"})
    
    if serializer.is_valid():
        user.set_password(request.data['password'])
        user.save()
        return Response({
            "message": "Password has succefully changed"
        })
    else:
        return Response(serializer.errors)

def RandomTokenGen():
    char = string.ascii_letters + string.digits
    rand_token = ''.join(random.choice(char) for i in range(50))

    return rand_token

@api_view(['POST'])
def ForgotPassword(request):
    
    token = RandomTokenGen()
    
    email = request.data["email"]
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = ""

    if user != "":
        data = {
            'user': user.id,
            'token': token
        }
        serializer = PasswordTokenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            html_content = render_to_string("forgot_password.html", data)
            email = EmailMessage(
                subject = 'Please reset your password',
                body = html_content,
                from_email = "Ferry Susanto UOW <ferry.milanisti22@gmail.com>",
                to = ["yohanesfersusanto@gmail.com"]
            )
            email.content_subtype = "html"
            time.sleep(2)
            email.send()
        else:
            return Response(serializer.errors)
        return Response(token)
    
    return Response({
        "message": "Email is incorrect!"
    })
    
@api_view(['GET', 'POST'])
def ResetPassword(request, token):
    if request.method == "POST":
        # verify token user
        tokenVal = PasswordToken.objects.filter(token=token, status=0)
 
        if len(tokenVal) > 0:
            tokenTime = tokenVal[0].create_date + timedelta(hours=3)
            
            # compare tokenTime with datetime now
            if tokenTime > datetime.now() and tokenVal[0].status == False:
                try:
                    user = User.objects.get(pk=tokenVal[0].user_id)
                except User.DoesNotExist:
                    return Response(status=404)
            
                serializer = ResetPasswordSerializer(data=request.data)
                
                if serializer.is_valid():
                    user.set_password(request.data['password'])
                    user.save()

                    tokenVal[0].status = True
                    tokenVal[0].save()
                    return Response({
                        "message": "Password has succefully changed"
                    }, status=200)
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response({"error"}, status=400)
        else:
            return Response({"mismatch": True}, status=400)
        
    
    if request.method == 'GET':
        tokenVal = PasswordToken.objects.filter(token=token, status=0)[0]

        # check if token is within 3 hours
        tokenTime = tokenVal.create_date + timedelta(hours=3)
        print(tokenTime)
        # compare tokenTime with datetime now
        if tokenTime > datetime.now() and tokenVal.status == False:
            return Response({"success"}, status=200)
        else:
            if tokenVal.status == False:
                tokenVal.status = True
                tokenVal.save()
            return Response({"error"}, status=400)

@api_view(['GET','POST','PUT'])
@csrf_exempt
def paymentInformation(request,user):
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        user = ""
    if user != "":
        try:
            paymentInformation = PaymentInformation.objects.get(user=user.id)
        except PaymentInformation.DoesNotExist:
            paymentInformation = ""

        if request.method == "POST":

            data = {
                "user": user.id,
                "credit_card": str(encryptString(request.data['credit_card'])),
                "expiry_date": str(encryptString(request.data['expiry_date'])),
                'cvv': str(encryptString(request.data['cvv']))  
            }

            if paymentInformation == "":
                serializer = PaymentInformationSerializer(data=data)
            else:
                serializer = PaymentInformationSerializer(paymentInformation, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'success', 'status': 200 }, status=200)
            else:
                return Response(serializer.errors, status=400)
            
        
        if request.method == 'GET':
            
            if paymentInformation !="":

                serializer = PaymentInformationSerializer(paymentInformation, many=False)

                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)    
    else:
        return Response("User cannot be found!")     
        
        
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def taskDetail(request, taskId):
#     try:
#         task = Task.objects.select_related('user').get(pk=taskId)
#     except Task.DoesNotExist:
#         return Response(status=404)
    
#     if request.method == 'GET':
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(task, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=200)
#         else:
#             print(serializer.errors)
#             return Response(status=404)

