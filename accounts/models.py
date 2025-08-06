from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,related_name= 'user_profile' ,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, unique= True, null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @receiver(post_save, sender= User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        


class Auther(models.Model):
    user = models.OneToOneField(User,related_name= 'user_Auther' ,on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Auther Profile"

