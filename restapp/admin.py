from django.contrib import admin

# Register your models here.
from restapp.models import FriendTable, ContactRequest, Message

admin.site.register(FriendTable)
admin.site.register(ContactRequest)
admin.site.register(Message)