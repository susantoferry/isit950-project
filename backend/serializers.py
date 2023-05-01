from rest_framework import serializers
from backend.models import *
from django.contrib.auth.password_validation import validate_password

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


# class ProfileSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Profile
#         fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'



class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(read_only=True, source='category.name')
    user_client_id = serializers.CharField(read_only=True, source='user.username')
    img_profile = serializers.CharField(read_only=True, source='user.img_profile')
    rating = serializers.FloatField(read_only=True, source='user.rating')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    task_title_to_url = serializers.CharField(read_only=True)
    my_bookmark = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
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
    # tasks = serializers.CharField(read_only=True, source='task')

    class Meta:
        model = Watchlist
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        
class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class UserSkillSerializer(serializers.ModelSerializer):
    users = serializers.CharField(read_only=True, source='user')
    skills = SkillSerializer(read_only=True, source="skill")
    
    class Meta:
        model = UserSkill
        fields = '__all__'

class PasswordTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordToken
        fields = '__all__'

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs