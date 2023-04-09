from django.urls import path
from . import views

urlpatterns=[
    path('send-message/<int:pk>', views.send_message),
    path('<int:pk>', views.get_message),
    path('last-message', views.get_user_last_message)
]