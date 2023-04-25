from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("category", views.category, name="category"),
    path("category/<int:id>", views.categoryDetail, name="category_detail"),
    path("question/<int:taskId>", views.question, name="question"),
    path("task", views.task, name="task"),
    path("task/<int:taskId>", views.taskDetail, name="task_detail"),
    path("show_my_watchlist/<str:user>", views.myWatchlist, name="show_my_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("skill", views.skill, name="skill"),
    path("skill/<int:id>", views.skillDetail, name="skill_detail"),
    path("membership", views.membership, name="membership"),
    path("membership/<int:id>", views.membershipDetail, name="membership_detail"),
    path("my_skilllist/<str:user>", views.mySkillList, name="show_my_skilllist"),
    path("paymentInformation/<str:user>", views.paymentInformation, name="paymentInformation"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)