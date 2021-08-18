from django.urls import path
from .views import *

urlpatterns = [
    path('restaurant/notifications/', NotificationDetail.as_view(), ),
    path('restaurant/notifications/read_all/', mark_all_notifications_as_read, ),
    path('restaurant/notifications/read/<int:pk>', mark_a_notification_as_read, ),

]
