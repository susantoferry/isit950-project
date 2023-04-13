from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return f"Category Id: {self.id}, Name: {self.name}"
    
class Offer(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="offer_task_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer_sp_id")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, Task ID: {self.task}, User Provider: {self.user}, price: {self.price}"


class Skill(models.Model): 
    skill_name = models.CharField(max_length=30)
    def __str__(self):
        return f"Id: {self.id}, Skill: {self.skill_name}"


class Membership(models.Model):
    package_name=models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"Id: {self.id}, Membership: {self.package_name}, Price: {self.price}"

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    location = models.CharField(max_length=80)
    location_link = models.CharField(max_length=100)
    completed_on = models.DateField()
    status = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_client", null=True)
    user_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_provider", null=True)
    is_paid = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    @property
    def my_bookmark(self):
        return [u.user for u in self.task_bookmark.all()]
    
    @property
    def task_title_to_url(self):
        task_title = self.task_title + " " + str(self.id)
        return task_title.replace(' ', '-')

    def __str__(self):
        return f"User: {self.user}, Category: {self.category}, Task: {self.task_title}"
    


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="question_task_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_user_id")
    question = models.TextField()
    parent_id = models.IntegerField(null=True)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task.id}, User: {self.user.id}, Parent Id: {self.parent_id}"

class Watchlist(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_bookmark")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task}, User: {self.user}"

        
class UserSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Id: {self.id}, Skill: {self.skill}, User: {self.user}"

