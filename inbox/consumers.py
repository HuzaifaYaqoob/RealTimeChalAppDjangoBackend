# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connected **********************************************')
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'inbox_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('Diconnected **********************************************')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )



    # Receive message from WebSocket
    def receive(self, text_data):
        print('Signal Received **********************************************')
        print(text_data)


        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username' : username,
                'date' : str(datetime.date.today())
                # 'first_name' : text_data_json['first_name'],
                # 'last_name' : text_data_json['last_name'],
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print('Signal received from chat **********************************************')

        print(event)
        message = event['message']
        username = event['username']
        print(message)
        print(username)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username' : username,
            'date' : str(datetime.date.today())
            # 'first_name' : event['first_name'],
            # 'last_name' : event['last_name'],
        }))