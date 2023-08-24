from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message
#user registered default

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)