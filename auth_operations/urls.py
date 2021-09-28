from django.urls import path
from . import views

urlpatterns = [
    path('api/password/change-password/', views.change_password, ),
    path('api/password/reset-password-request/',
         views.reset_password_request, ),
    path('api/password/reset-password/<uidb64>/<token>/',
         views.check_password_token, name='password_reset_token'),
    path('api/password/set-new-password/', views.set_new_password, ),

    path('auth/verify-email/', views.verify_email, name='verify_email'),

]
