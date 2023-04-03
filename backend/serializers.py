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

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    user_client_id = serializers.CharField(read_only=True, source='user.username')
    my_bookmark = serializers.CharField(read_only=True)  

    class Meta:
        model = Task
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(read_only=True, source="task")

    class Meta:
        model = Watchlist
        fields = '__all__'