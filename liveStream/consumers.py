import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('text_data_json>>>', text_data_json)
        message = text_data_json['message']
        sender = text_data_json['sender']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': {'message': message, 'sender': sender}
        }))


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['stream_key']
        if self.room_name:
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
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