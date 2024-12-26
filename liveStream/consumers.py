import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


stream_members = {}
class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['stream_key']
        self.user = self.scope['url_route']['kwargs']['user']
        if self.room_name:
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()

            if self.room_name in stream_members and self.user in stream_members[self.room_name]:
                await self.channel_layer.group_send(
                self.room_name,
                    {
                        'type': 'send.message',
                        'receive_dict': {
                            'action': 'error',
                            'target': self.user,
                            'message': f"Hi {self.user}, you can not join this stream with multiple browser!"
                        }
                    }
                )

            if self.room_name in stream_members:
                stream_members[self.room_name].append(self.user)
            else:
                stream_members[self.room_name] = [self.user]

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'send.message',
                    'receive_dict': {
                        'action': 'count-members',
                        'target': self.user,
                        'status': 'joined',
                        'members': len(stream_members[self.room_name])
                    }
                }
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

        should_close_room = await self.clear_stream()

        if should_close_room:
            del stream_members[self.room_name]
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'send.message',
                    'receive_dict': {
                        'action': 'close',
                        'message': f"The stream has been closed by Admin."
                    }
                }
            )
            return

        if self.room_name in stream_members:
            stream_members[self.room_name].remove(self.user)
            member_count = len(stream_members[self.room_name])

            if member_count <= 0:
                del stream_members[self.room_name]
                return

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'send.message',
                    'receive_dict': {
                        'action': 'count-members',
                        'target': self.user,
                        'status': 'left',
                        'members': len(stream_members[self.room_name])
                    }
                }
            )

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        action = receive_dict['action']

        if action == 'new-offer' or action == 'new-answer':
            receive_channel_name = receive_dict['message']['receive_channel_name']
            receive_dict['message']['receive_channel_name'] = self.channel_name

            await self.channel_layer.send(
            receive_channel_name,
                {
                    'type': 'send.message',
                    'receive_dict': receive_dict,
                }
            )

            return

        receive_dict['receive_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send.message',
                'receive_dict': receive_dict,
            }
        )

    async def send_message(self, event):
        receive_dict = event['receive_dict']
        await self.send(text_data=json.dumps({
            'message': receive_dict
        }))

    @sync_to_async
    def clear_stream(self):
        try:
            from django.contrib.auth.models import User
            from stream.models import Stream

            user = User.objects.get(username=self.user)
            if user.is_superuser:
                Stream.objects.filter(unique_key=str(self.room_name).strip()).first().delete()
                return True
        except Exception as e:
            return
