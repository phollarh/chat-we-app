from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('chat/', views.chat_preview, name='chat'),
    path('chat/<int:recipient_id>/', views.chatm_view, name='chatm'),
    path('get_private_message/', views.get_private_message, name='get_private_message'),
    path('save_messagePreviewto_db/', views.save_messagePreviewto_db, name='save_messagePreviewto_db'),
    path('get_recipient_details/', views.get_recipient_details, name='get_recipient_details'),
    path('send_message/', views.send_message, name='send_message'),
    path('upload_files/', views.upload_files, name='upload_files'),
    path('receive_sms/', views.receive_sms, name='receive_sms'),
    path('send_sms_to_external_user/', views.send_sms_to_external_user, name='send_sms_to_external_user'),
]

