from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout

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
    category = Category.objects.raw("SELECT * FROM backend_category")
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def task(request):
    if request.method == "GET":
        tasks = Task.objects.all().order_by("-modify_date")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=400)
        
        return Response(serializer.data)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def taskDetail(request):
    