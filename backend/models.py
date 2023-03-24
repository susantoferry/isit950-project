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

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    location = models.CharField(max_length=80)
    location_link = models.CharField(max_length=100)
    completed_on = models.DateField()
    status = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_user")
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"User: {self.user}, Category: {self.category}, Task: {self.task_title}"

class Watchlist(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task}, User: {self.user}"
