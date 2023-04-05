from django.contrib import admin

from people.models import FriendRequest, Friend

# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(Friend)