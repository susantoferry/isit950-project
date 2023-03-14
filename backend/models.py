from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return f"Name: {self.name}"
    
class PaymentType(models.Model):
    payment_type = models.CharField(max_length=20)

    def __str__(self):
        return f"Id:{self.id}, Type: {self.payment_type}"

