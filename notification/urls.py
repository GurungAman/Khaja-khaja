from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.Notifications.as_view(), ),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view(), ),
    path('notifications/read/<int:pk>/',
         views.mark_a_notification_as_read, ),
    #     path('notifications/read_all/',
    #          views.mark_all_notifications_as_read, ),

]
