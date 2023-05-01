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
    path("skill/<str:skillId>", views.skillDetail, name="skill_detail"),
    path("update_user/<str:user>", views.updateUserDetail, name="update_user_detail"),

    path("user_login", views.login, name="login"),
    path('add_user', views.AddUser, name="add_user"),
    path('change_password/<int:id>', views.ChangePassword, name="change_password"),
    path("forgot_password", views.ForgotPassword, name="forgot_password"),
    path("reset_password/<str:token>", views.ResetPassword, name="reset_password"),
    path("logout", knox_views.LogoutView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)