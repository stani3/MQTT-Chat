from django.db import models
from django.contrib.auth.models import User


from os.path import join as path_join

# Function to define the upload path for profile photos
def user_profile_photo_path(instance, filename):
    # Construct the upload path using the user's username
    return path_join('default/', instance.user.username, filename)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    photo = models.ImageField(upload_to= user_profile_photo_path, null=True, default='default/default.png')


    def __str__(self):
        return f'{ self.user.username } Profile'