from django.urls import path
from . import views
from .sub_views import college_view as cv

urlpatterns=[
    path('check-email', views.checkEmail),
    path('register', views.register),
    path('change-profile-picture', views.change_profile_picture),
    path('details/<int:pk>', views.user_details),
    path('test', views.test),
    path('colleges', cv.list_colleges),
    path('send-request/<int:pk>', cv.send_request_to_college),
    path('request-college', cv.list_request),
    path('action-request/<int:pk>', cv.take_action_to_request),
    path('college/<int:pk>', cv.college_detail),
    path('enrolled-colleges', cv.enrolled_college)
]