from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from backend.models import *
from .serializers import *

# Create your views here.

@api_view(['GET', 'POST'])
def index(request):
    # category = Category.objects.raw('SELECT * FROM')
    category = Category.objects.raw("SELECT * FROM backend_category")
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def category(request):
    if request.method == 'GET':
        category = Category.objects.raw("SELECT * FROM backend_category")
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

@api_view(['GET', 'POST'])
@csrf_protect 
def task(request):
    if request.method == 'GET':
        tasks = Task.objects.all().order_by("status","-modify_date")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        print("a")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=400)
        
        return Response(serializer.data)
    
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
           # watchlist.delete()
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