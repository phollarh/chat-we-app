import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Chats
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async

User = get_user_model()

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.preview_group_name = f'chat_preview_{self.user_id}'
       
        await self.accept()
        
        
        # Join the group
        await self.channel_layer.group_add(
            self.preview_group_name,
            self.channel_name
        )
        
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'recipient_id' in data:
            self.sender_id = self.scope['user'].id
            self.recipient_id =int( data['recipient_id'])
            self.get_user_phone_number = await sync_to_async(lambda: self.scope['user'].profile.phone_number)()
            self.is_external = data.get('is_external')
            self.group_name = f'private_chat_{min(self.sender_id, self.recipient_id)}_{max(self.sender_id, self.recipient_id)}'
            print(self.group_name)
        if 'sender_twilio_number' and 'recipient_phone_number' in data:
            self.get_user_phone_number = await sync_to_async(lambda: self.scope['user'].profile.phone_number)()
            print('the number is',self.get_user_phone_number)
            self.sender_id = self.scope['user'].id
            self.sender_phone_number = data.get('sender_twilio_number')
            self.recipient_phone_number = int(data.get('recipient_phone_number'))
            self.is_external = data.get('is_external')
            
            sorted_number=sorted([int(self.sender_phone_number), self.recipient_phone_number])
            self.group_name = f'private_chat_{sorted_number[0]}_{sorted_number[1]}'

            print(self.group_name)
          

            #join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
            )
        if 'message' in data:
        # Receive a message from WebSocket
        
            message = data['message']
            sender_id = self.scope['user'].id
            sender_number = str(self.get_user_phone_number)
            recipient_Id = data.get('recipient_Id')
            external_user=data.get('external_user')
            is_external_user= self.is_external
            timestamp = data['timestamp']
            file_url = data.get('file_url')
    
           
            await self.save_message(message,sender_id, recipient_Id,external_user,is_external_user, file_url )
            recipient_name = await self.get_recipient_name(recipient_Id, external_user)
            recipient_number = await self.get_recipient_number(recipient_Id, external_user)
        # Send the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'sender_number': sender_number,
                    'recipient_Id':recipient_Id,
                    'recipient_number':recipient_number,
                    'timestamp':timestamp,
                    'file_url':file_url,
                    'external_user':external_user,
                    'is_external_user':is_external_user
                }
            )
            
            
            await self.channel_layer.group_send(
                self.preview_group_name,
                {
                    'type': 'update_preview',
                    'message': message,
                    'sender_id': sender_id,
                    'sender_number':sender_number,
                    'recipient_Id': recipient_Id,
                    'recipient_number':recipient_number,
                    'timestamp' :timestamp,
                    'recipient_name':recipient_name,
                    'sender_name': self.scope['user'].first_name , # Get sender name for preview
                    'external_user':external_user,
                    'is_external_user':is_external_user
                })
           

            if sender_id != recipient_Id:
                await self.channel_layer.group_send(
                    f'chat_preview_{recipient_Id}',
                    {
                        'type': 'update_preview',
                        'message': message,
                        'sender_name': self.scope['user'].first_name,
                        'sender_id':  self.scope['user'].id,
                        'timestamp':timestamp,
                        'recipient_Id': recipient_Id,
                        # 'recipient_number':recipient_number,
                        'recipient_name':recipient_name
                    }
                )
                
          
    @sync_to_async
    def save_message(self, message, sender_id=None, recipient_id=None,external_user=None,is_external=False, file_url=None ):
        if self.is_external == True:
            if sender_id==None:

                recipient = get_object_or_404(get_user_model(), id=recipient_id)
                chat = Chats.objects.create(external_user=external_user, recipient=recipient, content=message ,is_external=True, image=file_url)
                chat.save()
            elif recipient_id==None:
                sender = get_object_or_404(get_user_model(), id=sender_id)

                chat = Chats.objects.create( sender=sender,external_user=external_user, content=message ,is_external=True, image=file_url)
                chat.save()
            
        else:
            sender = get_object_or_404(get_user_model(), id=sender_id)
            recipient = get_object_or_404(get_user_model(), id=recipient_id)

            chat = Chats.objects.create( sender=sender,recipient=recipient, content=message , image=file_url)
            chat.save()
    
    @sync_to_async
    def get_recipient_name(self, recipient_id, external_user=None):
        if recipient_id:

            recipient = get_object_or_404(get_user_model(), id=recipient_id)

            return recipient.first_name 
        else:
            return external_user
    @sync_to_async
    def get_recipient_number(self, recipient_id, external_user_number=None):
        if recipient_id:

            recipient = get_object_or_404(get_user_model(), id=recipient_id)

            return str(recipient.profile.phone_number)
        else:
            return external_user_number
    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.preview_group_name,
            self.channel_name
        )

        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
   
    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_number':event['sender_number'],
            'recipient_Id': event['recipient_Id'],
            'recipient_number':event.get('recipient_number'),
            'timestamp':event['timestamp'],
            'file_url': event.get('file_url'),
            'is_external_user':event['is_external_user']
        }))

    async def update_preview(self, event):
        # Send the updated preview to WebSocket
        await self.send(text_data=json.dumps({
            'preview_message': event['message'],
            'sender_name': event['sender_name'],
            'timestamp':event['timestamp'],
            'recipient_id': event['recipient_Id'],
            'sender_id': event['sender_id'],
            'sender_number':event.get('sender_number'),
            'recipient_name':event['recipient_name'],
            'recipient_number':event.get('recipient_number'),
            'external_user': event.get('external_user'),
            'is_external_user':event.get('is_external_user')

        }))