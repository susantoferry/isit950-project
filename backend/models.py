from django.db import models
from django.contrib.auth.models import AbstractUser
import geocoder
# Create your models here.

mapbox_token = 'pk.eyJ1IjoiZnM3OTQiLCJhIjoiY2xneW1lZmNmMGI0NTN0cDkyeHpzdzgwZyJ9.V74wwUIzF1J3tVUg3tdcXg'

class Membership(models.Model):
    package_name=models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"Id: {self.id}, Membership: {self.package_name}, Price: {self.price}"

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

    @property
    def task_title_to_url(self):
        task_title = self.task.task_title + " " + str(self.task.id)
        return task_title.replace(' ', '-')

    def __str__(self):
        return f"Id: {self.id}, Task ID: {self.task}, User Provider: {self.user}, price: {self.price}"

class Skill(models.Model): 
    skill_name = models.CharField(max_length=30)
    def __str__(self):
        return f"Id: {self.id}, Skill: {self.skill_name}"
    
class Price(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="category_price")
    price = models.DecimalField(max_digits=6, decimal_places=0, default=0)

    def __str__(self):
        return f"Id: {self.id}, Category: {self.category.id}, Price: {self.price}"

class Task(models.Model):
    task_title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    booking_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
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
    
    @property
    def user_provider_name(self):
        user_provider = self.user_provider.username
        return user_provider

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
    credit_card =models.CharField(max_length=255)
    expiry_date=models.CharField(max_length=255)
    cvv=models.CharField(max_length=255)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, User: {self.user}"
    
class Notification(models.Model):
    content_notif = models.IntegerField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_notification", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notif")
    user_sp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sp", blank=True, null=True)
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task.id}"
    
class MembershipTransaction(models.Model):
    membership = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trans_user_id")
    trans_type = models.CharField(max_length=1, null=True)
    credit_card =models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Id: {self.id}, Membership: {self.membership}, User: {self.user}"

class Review(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_review")
    comment_sp = models.TextField(null=True, blank=True)
    comment_client = models.TextField(null=True, blank=True)
    rating_sp = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=True, blank=True)
    rating_client = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=True, blank=True)
    user_sp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rev_user_sp", null=True)
    user_client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rev_user_client", null=True)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"Id: {self.id}, Task: {self.task}"
    
class Transaction(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_trans")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_trans")
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True)
    admin_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, null=True)
    is_payee = models.BooleanField(default=0, null=True)
    create_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Id: {self.id}, Task: {self.task}, User SP: {self.user_sp.id}, Client: {self.user_client.id}"
