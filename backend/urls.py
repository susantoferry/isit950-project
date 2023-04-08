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
    path("skill/<str:skillId>", views.skillDetail, name="skill_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)