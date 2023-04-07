from django.contrib import admin

from publication.models import Publication, PublicationLike, PublicationComment

# Register your models here.
admin.site.register(Publication)
admin.site.register(PublicationLike)
admin.site.register(PublicationComment)