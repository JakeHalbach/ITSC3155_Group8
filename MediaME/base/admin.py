from django.contrib import admin

# Register your models here.
from .models import Media, Type, Creator, Genre, Room, Message

admin.site.register(Media)
admin.site.register(Type)
admin.site.register(Creator)
admin.site.register(Genre)
admin.site.register(Room)
admin.site.register(Message)
