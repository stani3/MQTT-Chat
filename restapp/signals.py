from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendTable, ContactRequest


# @receiver(post_save, sender=FriendTable)
# def create_reverse_friendship(sender, instance, created, **kwargs):
#     if created:
#         # If a new friendship is created, automatically create the reverse friendship
#         FriendTable.objects.create(owner=instance.friend, friend=instance.user)


# @receiver(post_save, sender=ContactRequest)
# def accept_friend(sender, isntance, created, **kwargs):
#     FriendTable.objects.create()