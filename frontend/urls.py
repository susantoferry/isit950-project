from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<taskId>", views.taskDetail, name="tasks"),
    path("watchlist", views.watchlist, name="watchlist"),
    # path("login", views.loginView, name="login"),
    # path("logout", views.logoutView, name="logout"),
    # path("change_password", views.changePassword, name="change_password"),
    # path("forgot_password", views.forgotPassword, name="forgot_password"),
    # path("forgot_password/<str:token>", views.forgotPassword_token, name="forgot_password"),
    # path("reset_password/<str:token>", views.resetPassword, name="resetPassword"),
]
