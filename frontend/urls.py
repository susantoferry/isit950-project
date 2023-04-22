from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_task", views.createTask, name="create_task"),
    path("my_task", views.myTask, name="my_task"),
    path("my_task/<int:taskId>", views.myTaskDetail, name="my_task"),
    path("my_watchlist", views.watchlist, name="my_watchlist"),
    path("account/profile", views.profile, name="profile"),
    path("select_sp/<taskId>", views.myTaskDetail, name="select_sp"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<slug:slug>", views.taskDetail, name="tasks"),
    path("test", views.testHTML, name="test_page"),
    path("login", views.loginView, name="login"),
    path("forgot_password", views.forgotPassword, name="forgot_password"),
    path("sign_up", views.signUp, name="sign_up"),
    # path("logout", views.logoutView, name="logout"),
    # path("change_password", views.changePassword, name="change_password"),
    
    # path("forgot_password/<str:token>", views.forgotPassword_token, name="forgot_password"),
    # path("reset_password/<str:token>", views.resetPassword, name="resetPassword"),
]
