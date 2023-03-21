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