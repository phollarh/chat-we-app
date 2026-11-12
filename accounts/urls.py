from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page, name='homepage'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('email_confirmation/', views.EmailConfirmPage, name='email_confirmation'),
    path('profile_view/<str:username>',views.Profile_view, name='profile_view'),
    path('send_profile_Id/',views.send_profile_Id, name='send_profile_Id'),
    path('save_cropped_image/',views.save_cropped_image, name='save_cropped_image'),
    path('logout/', views.logout_user, name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]
