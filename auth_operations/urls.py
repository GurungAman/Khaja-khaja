from django.urls import path
from . import views

urlpatterns = [
    path('api/password/change_password/', views.change_password, ),
    path('auth/verify-email/', views.verify_email, name='verify-email'),

]
