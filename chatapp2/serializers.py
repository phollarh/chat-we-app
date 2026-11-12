
from rest_framework import serializers
from .models import Chats

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = [ 'sender', 'recipient', 'content', 'timestamp']
