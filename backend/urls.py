from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("category", views.category, name="category"),
    path("category/<int:id>", views.categoryDetail, name="category_detail"),
    path("offer", views.offer, name="offer"),
    path("offer/<int:taskId>", views.offerDetail, name="offer_detail"),
    path("question/<int:taskId>", views.question, name="question"),
    path("my-task/accept-offer/<taskId>/<userSPId>", views.acceptOffer, name="accept_offer"),
    path("task", views.task, name="task"),
    path("task/<int:taskId>", views.taskDetail, name="task_detail"),
    path("get_my_task/<int:userId>", views.getMyTask, name="get_my_task"),
    path("show_my_watchlist/<str:user>", views.myWatchlist, name="show_my_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("getnotification/<int:userId>", views.notification, name="getnotification"),
    path("getnotificationID/<int:userId>/<notificationID>", views.notificationID, name="getnotificationID"),
    path("getreview/<int:reviewId>", views.review, name="getreview"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)