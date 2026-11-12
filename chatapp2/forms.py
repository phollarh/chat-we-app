from django import forms
from .models import Chats


class Chatform(forms.ModelForm):
    class Meta:
        model = Chats
        fields = ['recipient', 'content']