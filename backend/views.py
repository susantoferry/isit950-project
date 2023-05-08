from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
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
        im = im.convert('RGB')
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
        print(request.data)
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
                elif i == 'img_background':
                    saveUser.update({i: make_thumbnail(request.FILES[i], "", 'profiles_bg')})
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
    
@api_view(['GET', 'POST'])
def question(request, taskId):
    if request.method == 'GET':
        questions = Question.objects.filter(task_id=taskId).order_by("-modify_date")
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def offer(request):
    # if request.method == 'GET':
    #     offers = Offer.objects.all().order_by("status","-modify_date")
    #     serializer = OfferSerializer(offers, many=True)
    #     return Response(serializer.data)
    
    if request.method == 'POST':
        request.data["task"] = request.data["task"].rsplit('-', 1)[-1]

        request.data['user'] = User.objects.values_list('id', flat=True).get(username=request.data['user'])
        
        serializer = OfferSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "message": "Saved successfully"})
        else:
            return Response(serializer.errors,status=400)

@api_view(['GET', 'POST'])        
def notification(request):
    return
    

@api_view(['GET'])
def offerDetail(request, taskId):
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
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def taskDetail(request, taskId):

    taskId = taskId.rsplit('-', 1)[-1]
    
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
def membership(request):
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
def membershipDetail(request, id):
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
            userskill=UserSkill.objects.get(user=user.id,skill=request.data.get('skill'))
            userskill.delete()
            return Response(status=204)

        if request.method == "POST":
            skill = request.data.get('skill')
            if (Skill.objects.filter(id=skill).exists()):
            # checkUserId = User.objects.filter(pk=user.id)
            # Check if User Id Exists
            # if checkUserId.count() > 0:
                # Preventing duplicating data if user id and skill id already exist in table
                checkData = UserSkill.objects.filter(user=user.id, skill=skill)
                if checkData.count() == 0:
                    data = {
                        "user": user.id,
                        "skill": skill
                        }
                    serializer = UserSkillSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors)
                    return Response(serializer.data)
                else:
                    return Response("Error. Duplicate data when adding new skill")
            else:
                return Response("skill  not exists")
    else:
        return Response("User cannot be found!")
    
@api_view(['GET', 'PUT', 'DELETE'])
def membershipDetail(request, id):
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
            return Response(serializer.data)

        if request.method == 'DELETE':
            userskill=UserSkill.objects.get(user=user.id,skill=request.data.get('skill'))
            userskill.delete()
            return Response(status=204)

        if request.method == "POST":
            skill = request.data.get('skill')
            if (Skill.objects.filter(id=skill).exists()):
            # checkUserId = User.objects.filter(pk=user.id)
            # Check if User Id Exists
            # if checkUserId.count() > 0:
                # Preventing duplicating data if user id and skill id already exist in table
                checkData = UserSkill.objects.filter(user=user.id, skill=skill)
                if checkData.count() == 0:
                    data = {
                        "user": user.id,
                        "skill": skill
                        }
                    serializer = UserSkillSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors)
                    return Response(serializer.data)
                else:
                    return Response("Error. Duplicate data when adding new skill")
            else:
                return Response("skill  not exists")
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
            # token = AuthToken.objects.create(user)[1]
            
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
            else:
                return Response(serializer.errors, status=400)
            return Response({'message': 'success', 'status': 200 }, status=200)
        
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

