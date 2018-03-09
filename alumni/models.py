from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    approved_post = models.BooleanField(default=False)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve(self):
        self.approved_post = True
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('alumni.Post', related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

curr=datetime.datetime.now().year
YEARS=[]
for i in range(1997 ,curr+4):
    dum=[(i, str(i))]
    YEARS=YEARS+dum
class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank = True)
    roll_no=models.IntegerField(default=160123005, blank=True,)
    profile_img = models.ImageField(upload_to='profile_img', default="profile_img/profile.png")
    passout_year = models.IntegerField(default=2016, blank=True, choices=YEARS)
    fb_link = models.URLField(null=True)
    ln_link = models.URLField(null=True)
    curr_work = models.CharField(max_length=100, blank = True)
    prev_work = models.CharField(max_length=200, blank = True)
    def __str__(self):
        return self.name



