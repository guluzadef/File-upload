import json

from base_user.models import MyUser
from asgiref.sync import async_to_sync

from todo_app.models import File
from django.utils import timezone
from .mongo_client import Repo

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection


class UserSpecChat(AsyncWebsocketConsumer):
    # Connection to socket channel
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'notification_%s' % self.room_name
        self.user = self.scope['user']
        self.file_id = self.room_name
        # Repo.delete("comments")
        # Join room group
        if self.user.username:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            comments = Repo.search("comments", {
                "user_id": self.user.id,
                "file_id": self.file_id
            })
            await self.send(text_data=json.dumps({
                "status": "list",
                "data": comments
            }))
        else:
            raise DenyConnection("Only Authorized user can connect socket")

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        comment = text_data['comment']
        now = timezone.now()
        data = {
            "user_id": self.user.id,
            "file_id": self.file_id,
            "profile_url": self.user.get_profile_img(),
            "username": self.user.username,
            "create_date": now.strftime("%m/%d/%Y, %H:%M"),
            "comment": comment
        }
        response = Repo.save("comments", data)
        await self.send(text_data=json.dumps({
            "msg": "Comment created"
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_notification',
                'message': {
                    "status": "new",
                    "data": response
                }
            }
        )
#munis he gozde mongonun icindekinide atim saveni
    # Receive message from all connected room group
    async def send_notification(self, event):
        data = event['message']
        print(data)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    # when user disconnected from socket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )