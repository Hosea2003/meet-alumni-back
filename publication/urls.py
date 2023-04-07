from django.urls import path
from . import views

urlpatterns=[
    path('create', views.publish),
    path('like/<int:pk>', views.like_or_dislike_post),
    path('comment/<int:pk>', views.comment_post),
    path('comments/<int:pk>', views.view_comments),
    path('posts', views.get_posts)
]