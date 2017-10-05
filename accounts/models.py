from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

curr=datetime.datetime.now().year
YEARS=[]
for i in range(2000, curr+1):
    dum=[(i, str(i))]
    YEARS=YEARS+dum

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.IntegerField(default=2016, blank=True, choices=YEARS)
    fb_link = models.URLField(null=True)
    ln_link = models.URLField(null=True)
    curr_work = models.CharField(max_length=100, blank = True)
    prev_work = models.CharField(max_length=200, blank = True)
    pro_img = models.ImageField(upload_to = 'images/', default="/static/default_pro_pic.png")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
