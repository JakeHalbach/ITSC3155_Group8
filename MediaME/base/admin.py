from django.contrib import admin

# Register your models here.
from .models import media, Type, creator

admin.site.register(media)
admin.site.register(Type)
admin.site.register(creator)
