from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'sender','receiver')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
	list_display = ('creator', 'date_creation')

@admin.register(RouteMessageJournal)
class RouteMessageJournalAdmin(admin.ModelAdmin):
	list_display = ('prev_user', 'next_user', 'message_id', 'route_id', 'date')

@admin.register(UserInRoute)
class UserInRouteAdmin(admin.ModelAdmin):
	list_display = ('route', 'prevus', 'nextus', 'u_sequence')


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
	list_display = ('title', 'file')

@admin.register(Tags)
class TemplatesAdmin(admin.ModelAdmin):
	list_display = ('tag', 'name_tag')



