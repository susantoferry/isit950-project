from rest_framework import serializers
from backend.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(source='user')

    class Meta:
        model = Task
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(source='task')

    class Meta:
        model = Watchlist
        fields = '__all__'