from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_task", views.createTask, name="create_task"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<slug:slug>", views.taskDetail, name="tasks"),
    path("my_task", views.myTask, name="my_task"),
    path("my_task/<int:taskId>", views.myTaskDetail, name="my_task"),
    path("select_sp/<taskId>/<userId>", views.myTaskDetail, name="select_sp"),
    
    path("my_watchlist", views.watchlist, name="my_watchlist"),
    # path("login", views.loginView, name="login"),
    # path("logout", views.logoutView, name="logout"),
    # path("change_password", views.changePassword, name="change_password"),
    # path("forgot_password", views.forgotPassword, name="forgot_password"),
    # path("forgot_password/<str:token>", views.forgotPassword_token, name="forgot_password"),
    # path("reset_password/<str:token>", views.resetPassword, name="resetPassword"),
]
