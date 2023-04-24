from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("account/notification", views.notification, name="notification"),
    path("account/payment-method", views.paymentMethod, name="payment_method"),
    path("account/payment-history", views.paymentHistory, name="payment_history"),
    path("account/profile", views.profile, name="profile"),
    path("account/wishlist", views.wishlist, name="my_wishlist"),

    path("create-task", views.createTask, name="create_task"),
    path("my-task", views.myTask, name="my_task"),
    path("my-task/<int:taskId>", views.myTaskDetail, name="my_task"),
    path("my-watchlist", views.watchlist, name="my_watchlist"),
    path("select-sp/<taskId>", views.myTaskDetail, name="select_sp"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<slug:slug>", views.taskDetail, name="tasks"),
    
    path("test123", views.testRead, name="test123"),

    path("test", views.testHTML, name="test_page"),
    path("login", views.loginView, name="login"),
    path("forgot_password", views.forgotPassword, name="forgot_password"),
    path("sign_up", views.signUp, name="sign_up"),
    path("logout", views.logout_view, name="logout"),
    
    # path("logout", views.logoutView, name="logout"),
    # path("change_password", views.changePassword, name="change_password"),
    
    # path("forgot_password/<str:token>", views.forgotPassword_token, name="forgot_password"),
    # path("reset_password/<str:token>", views.resetPassword, name="resetPassword"),
]
