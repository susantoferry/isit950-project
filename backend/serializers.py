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
    category_name = serializers.CharField(read_only=True, source='category.name')
    user_client_id = serializers.CharField(read_only=True, source='user.username')
    my_bookmark = serializers.CharField(read_only=True)
    task_title_to_url = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    user_provider = serializers.CharField(read_only=True, source='user.username')
    class Meta:
        model = Offer
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(read_only=True, source="task")

    class Meta:
        model = Watchlist
        fields = '__all__'