from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name="main"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/", Mail.as_view(), name="messages"),
    path("compose/", Compose.as_view(), name="compose"),
]
