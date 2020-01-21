from django.urls import path

from todo_app import consumers

websocket_urlpatterns = [
    path('comment/<int:id>', consumers.UserSpecChat)
]
