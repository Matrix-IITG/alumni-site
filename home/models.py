from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=30, blank=True, default='')
#     name = models.CharField(max_length=30, blank=True,)
#     # name = forms.CharField(max_length=30, required=True)
#     fb_link = models.URLField(blank=True,)
#     ln_link = models.URLField(blank=True,)
#     curr_work = models.CharField(max_length=100, blank=True,)
#     prev_work = models.CharField(max_length=200, blank=True,)