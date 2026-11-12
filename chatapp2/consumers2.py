import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
 let tsest = document.querySelector('ul.testing');
   
    document.addEventListener('newMessage', (e) => {
        console.log('New message received:', e.detail);
        const prevs = e.detail;
        prevs.forEach((message) => {
            
            const ki = `<li>${message.preview_message}</li>`;
            
            tsest.insertAdjacentHTML('afterbegin', ki);
        });
    });
    function triggerNewMessageEvent(filteredmessage) {
        const event = new CustomEvent('newMessage', { detail: filteredmessage });
        document.dispatchEvent(event); // Dispatch the custom event globally
    }
  

    // Simulating a new filteredmessage
    function receiveNewFilteredMessage(filteredmessage) {
        triggerNewMessageEvent(filteredmessage); // Trigger the event when a new message is received
    }
    const newMessage = arrayFilter
    receiveNewFilteredMessage(newMessage);

# //User = get_user_model()

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['user'].id
        self.recipient_id = int(self.scope['url_route']['kwargs']['recipient_id'])
        self.group_name = f'private_chat_{min(self.sender_id, self.recipient_id)}_{max(self.sender_id, self.recipient_id)}'

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient_id = text_data_json['recipient_Id']
        sender_id = self.scope['user'].id

        # Send message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'recipient_id': recipient_id
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'recipient_id': event['recipient_id']
        }))
