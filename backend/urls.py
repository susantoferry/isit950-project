from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("category", views.category, name="category"),
    path("category/<int:id>", views.categoryDetail, name="category_detail"),
    path("task", views.task, name="task"),
    path("task/<int:taskId>", views.taskDetail, name="task_detail"),
    # path("my_watchlist", views.myWatchlist, name="my_watchlist"),
    path("watchlist/<str:user>", views.watchlist, name="watchlist"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)