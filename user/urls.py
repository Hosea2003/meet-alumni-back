from django.urls import path
from . import views
from .sub_views import college_view as cv
from .sub_views import user_view as uv

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
    path('enrolled-colleges', cv.enrolled_college),
    path('other-colleges', cv.other_colleges),

    path('about/<int:pk>', uv.about),
    path('album/<int:pk>', uv.album),
    path('update', uv.update_info),
    path('change-password', uv.change_password)
]