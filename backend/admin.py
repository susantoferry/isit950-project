from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Offer)
admin.site.register(Task)