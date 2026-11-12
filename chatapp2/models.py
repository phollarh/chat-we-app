from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

# Create your models here.


class Chats(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages' , null=True, blank=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    external_user= models.CharField(max_length=15, blank=True, null=True , help_text="Phone number of the external user")
    is_external = models.BooleanField(default=False) 
    content = models.TextField()
    image=models.ImageField(null=True, blank=True, upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_external:
        # Case when there is an external user
            if self.sender is None:
            # External user is the sender
                return f"Chat from {self.external_user} to {self.recipient}"
            else:
            # External user is the recipient
                return f"Chat from {self.sender} to {self.external_user}"
        else:
        # Standard case: both sender and recipient are registered users
            return f"Chat from {self.sender} to {self.recipient}"

    





class ChatPreview(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_previews', on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), related_name='received_previews', on_delete=models.CASCADE)
    image=models.ImageField(null=True, blank=True, upload_to='images/')
    preview_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient')

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.preview_message}"


