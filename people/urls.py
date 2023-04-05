from django.urls import path
from . import views

urlpatterns=[
    path('friends',views.get_friends),
    path('send-friend-request/<int:pk>', views.send_request),
    path('friends-request', views.get_friends_request),
    path('accept-request/<int:pk>', views.accept_friend),
    path('college-members/<int:pk>', views.get_college_member)
]