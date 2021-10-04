from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronomic = models.CharField(max_length=100, blank=True,null=True,default=None)
    phone = models.CharField(max_length=30, blank=True)
    subscribe_news = models.BooleanField(default=None, blank=True, null=True)
    private_key=models.BinaryField(null=True)

class Center(models.Model):
    DATABASES = 'center'
    user = models.CharField(max_length=100, blank=True)
    public_key = models.BinaryField(null=True)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()