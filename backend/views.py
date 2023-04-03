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
            watchlist.delete()
            return Response({
                "success"
            }, status=200)
    
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