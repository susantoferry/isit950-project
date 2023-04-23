from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.generics import UpdateAPIView
from backend.models import *
from .serializers import *

from PIL import Image 

import os
import time
import uuid

from io import BytesIO
import base64

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
    
@api_view(['PUT'])
def updateUserDetail(request, user):
    if request.method == 'PUT':
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response(status=404)
        
        # img_profile = request.FILES.get('img_profile', "")
        # img_background = request.FILES.get('img_background', "")
        saveUser = {}
        if user != "":
            for i in request.data:
                if i == 'img_profile':
                    saveUser.update({i: make_thumbnail(request.FILES[i], "", 'profiles')})
                elif i == 'img_background':
                    saveUser.update({i: make_thumbnail(request.FILES[i], "", 'profiles_bg')})
                else:
                    saveUser.update({i: request.data[i]})

            serializer = UserSerializer(user, data=saveUser)
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
    if request.method == 'GET':
        offers = Offer.objects.all().order_by("status","-modify_date")
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
    

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
            watchlist = Watchlist.objects.get(task=task, user=user)
        except Watchlist.DoesNotExist:
            watchlist = ""

        if watchlist == "":
            serializer = WatchlistSerializer(data=request.data)

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
        skill = Skill.objects.raw("SELECT * FROM backend_skill")
        #skill = Skill.objects.all()
        serializer = SkillSerializer(skill, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        
        serializer = SkillSerializer(data=request.data)
        #print(request.data)
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

        



    
        
        
        
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def skillDetail(request, skillId):
    skill = Skill.objects.raw("SELECT * FROM backend_skill WHERE id = %s", [id])
    #skill = Skill.objects.get(id=id)
    if request.method == 'GET':
        serializer = SkillSerializer(skill, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)

        serializer = SkillSerializer(skill, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        skill.delete()
        return Response(status=status.HTTP_2O4_NO_CONTENT)

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