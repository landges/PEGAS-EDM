from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'sender','receiver')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id',)