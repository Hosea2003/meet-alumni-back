from django.contrib import admin
from .models import User, College, CollegeUser, ProfilePicture

# Register your models here.
admin.site.register(User)
admin.site.register(College)
admin.site.register(CollegeUser)
admin.site.register(ProfilePicture)
