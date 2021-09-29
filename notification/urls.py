from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/notifications/', views.Notifications.as_view(), ),
    path('restaurant/notification/<int:pk>/', views.NotificationDetail.as_view(), ),
    path('restaurant/notifications/read_all/',
         views.mark_all_notifications_as_read, ),
    path('restaurant/notifications/read/<int:pk>',
         views.mark_a_notification_as_read, ),

]
