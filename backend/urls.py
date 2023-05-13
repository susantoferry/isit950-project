from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from knox import views as knox_views

from . import views

urlpatterns = [
    path("category", views.category, name="category"),
    path("category/<int:id>", views.categoryDetail, name="category_detail"),
    path("offer", views.offer, name="offer"),
    path("offer/<int:taskId>", views.offerDetail, name="offer_detail"),
    path("question/<int:taskId>", views.question, name="question"),
    path("my-task/accept-offer/<taskId>/<userSpId>", views.acceptOffer, name="accept_offer"),
    path("task", views.task, name="task"),
    path("task/<slug:taskId>", views.taskDetail, name="task_detail"),
    re_path(r"^search_task/$", views.taskSearch, name="task_search"),
    path("get_my_task/<int:userId>", views.getMyTask, name="get_my_task"),
    path("show_my_watchlist/<str:user>", views.myWatchlist, name="show_my_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("skill", views.skill, name="skill"),
    path("skill/<int:id>", views.skillDetail, name="skill_detail"),
    path("membership", views.membership, name="membership"),
    path("membership/<int:id>", views.membershipDetail, name="membership_detail"),
    path("my_skilllist/<str:user>", views.mySkillList, name="show_my_skilllist"),
    path("paymentInformation/<str:user>", views.paymentInformation, name="paymentInformation"),
    # path("get_profile", views.getProfile, name="get_profile"),
    # path("get_profile/<profileId>", views.getProfileDetail, name="get_profile_detail")

    path("profile_api/<str:user>", views.userProfile, name="profile_api"),

    path("user_login", views.userLogin, name="user_login"),
    path('register_api', views.userRegister, name="register_api"),
    path('resend_email_api', views.resendEmailAPI, name="resend_email_api"),
    path('verifying-email-api', views.verifyingEmailAPI, name="verifying_email_api"),
    path('change_password/<int:id>', views.ChangePassword, name="change_password"),
    path("forgot_password_api", views.ForgotPassword, name="forgot_password_api"),
    path("reset_password_api/<str:token>", views.ResetPassword, name="reset_password_api"),
    path("logout", knox_views.LogoutView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)