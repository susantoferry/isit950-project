from django.db import models
from django.contrib.auth.models import AbstractUser
import geocoder
# Create your models here.

mapbox_token = 'pk.eyJ1IjoiZnM3OTQiLCJhIjoiY2xneW1lZmNmMGI0NTN0cDkyeHpzdzgwZyJ9.V74wwUIzF1J3tVUg3tdcXg'

# class Membership(models.Model):
#     package_name=models.CharField(max_length=30)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     create_date = models.DateTimeField(null=True)
#     modify_date = models.DateTimeField(null=True)
    
#     def __str__(self):
#         return f"Id: {self.id}, Membership: {self.package_name}, Price: {self.price}"

class User(AbstractUser):
    img_profile = models.CharField(max_length=100, null=True, blank=True)
    img_background = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(default="-", max_length=10, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=True, blank=True)
    email_verified = models.BooleanField(default=0, null=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return f"Category Id: {self.id}, Name: {self.name}"
    
class Offer(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="offer_task_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer_sp_id")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    admin_fee = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    description = models.TextField()
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, Task ID: {self.task}, User Provider: {self.user}, price: {self.price}"
    
# class Profile(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     gender = models.IntegerField(default=0)
#     address = models.TextField()
#     rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
#     img_profile = models.CharField(max_length=100, blank=True, null=True)
#     membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="membership_id", blank=True, null=True)
#     user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile_id")
#     create_date = models.DateTimeField(blank=True, null=True)
#     modify_date = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"Id: {self.id}, User: {self.user_profile}, Name: {self.first_name}"


# notif id, user id, task id, is_read, notif_type
# 1, 2, 2,0,1


class Skill(models.Model): 
    skill_name = models.CharField(max_length=30)
    def __str__(self):
        return f"Id: {self.id}, Skill: {self.skill_name}"

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    location = models.TextField(null=True)
    location_link = models.CharField(max_length=100, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    completed_on = models.DateField()
    status = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_client", related_query_name="profile", null=True)
    user_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_provider", null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.location, key=mapbox_token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Task, self).save(*args, **kwargs)

    @property
    def my_bookmark(self):
        # print([u.user for u in self.task_bookmark.all()])
        return [u.user for u in self.task_bookmark.all()]
    
    @property
    def task_title_to_url(self):
        task_title = self.task_title + " " + str(self.id)
        return task_title.replace(' ', '-')

    def __str__(self):
        return f"Id: {self.id}, User: {self.user}, Category: {self.category}, Task: {self.task_title}, Paid: {self.is_paid}, User: {self.user}"
    


class Question(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="question_task_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question_user_id")
    question = models.TextField()
    parent_id = models.IntegerField(null=True)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task}, User: {self.user.id}, Parent Id: {self.parent_id}"

class Watchlist(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_bookmark")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookmark")

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task.id}, User: {self.user}"



class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)

class UserSkill(models.Model):
    skill = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Id: {self.id}, Skill: {self.skill}, User: {self.user}"
    
class PasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userToken")
    token = models.CharField(max_length=60)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user}, Status: {self.status}"

class PaymentInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_paymentinfo", null=True)
    credit_card =models.CharField(max_length=50)
    expiry_date=models.CharField(max_length=50)
    cvv=models.CharField(max_length=50)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, User: {self.user}"
