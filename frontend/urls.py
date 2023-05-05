from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.utils.http import urlencode
from django.urls import include, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("account/notification", views.notification, name="notification"),
    path("account/payment-method", views.paymentMethod, name="payment_method"),
    path("account/payment-history", views.paymentHistory, name="payment_history"),
    path("account/profile", views.profile, name="profile"),
    path("account/profile-form", views.createProfile, name="profile_form"),
    path("account/edit-profile", views.editProfile, name="edit_profile"),
    path("account/wishlist", views.wishlist, name="my_wishlist"),

    path("create-task", views.createTask, name="create_task"),
    path("my-task", views.myTask, name="my_task"),
    path("my-task/<int:taskId>", views.myTaskDetail, name="my_task"),
    path("my-watchlist", views.watchlist, name="my_watchlist"),
    path("select-sp/<taskId>", views.myTaskDetail, name="select_sp"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/?name=<slug>", views.taskDetail, name="tasks"),
    re_path(r'^task/task_state/$', views.searchTask, name='task_state'),

    path("test123", views.testRead, name="test123"),

    path("verify-email/<email>", views.verifyEmail, name="verify_email"),
    path("verifying-email/<email>", views.verifyingEmail, name="verifying_email"),
    path("resend_email/<email>", views.resendEmail, name="resend_email"),

    path("postTask", views.postTask, name="postTask"),
    path("test2", views.test2HTML, name="test_page"),
    path("test3", views.test3HTML, name="test_page"),
    path("login", views.loginView, name="login"),
    path("register", views.registerView, name="register"),
    path("forgot-password", views.forgotPass, name="forgot_password"),
    path("reset-password/<token>", views.resetPass, name="reset_password"),
    path("logout", views.logout_view, name="logout"),
    
    # path("logout", views.logoutView, name="logout"),
    # path("change_password", views.changePassword, name="change_password"),
    
    # path("forgot_password/<str:token>", views.forgotPassword_token, name="forgot_password"),
    # path("reset_password/<str:token>", views.resetPassword, name="resetPassword"),
]
