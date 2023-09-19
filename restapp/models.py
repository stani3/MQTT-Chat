from django.core.exceptions import ValidationError
from django.db import models
import datetime
# Create your models here.
from users.models import Profile




MESSAGE_STATUS = [
    (1, 'Sent'),
    (2, 'Seen'),
    (3, 'FAILED'),
]

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)
    status = models.IntegerField(choices=MESSAGE_STATUS, default=1)

class FriendTable(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend')
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.user.username} ---> {self.friend.user.username}'


STATUS_TYPE = [
    (1, 'Pending'),
    (2, 'Accepted'),
    (3, 'Declined'),

]
class ContactRequest(models.Model):
    requester = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requester')
    pending_friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pending_friend')
    date_added = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_TYPE, default=1)


    def __str__(self):
        return f'{self.requester.user.username} ---> {self.pending_friend.user.username}'