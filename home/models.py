from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as translate
from django.utils.timezone import now
from django.contrib.auth.models import PermissionsMixin
from django.db import models

HOSTEL_CHOICES = (
    ('Siang','Siang'),
    ('Lohit' , 'Lohit'),
    ('Manas', 'Manas'),
    ('Dhing', 'Dhing'),
    ('Barak', 'Barak'),
    ('Umiam', 'Umiam'),
    ('Subhansari', 'Subhansari'),
    ('Dibang', 'Dibang'),
    ('Kapili', 'Kapili'),
    ('Dhansari', 'Dhansari'),
)


class AutoCreatedUpdatedMixin(models.Model):

    created_at = models.DateTimeField(
        verbose_name=translate('created at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=translate('updated at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = now()
            self.updated_at = self.created_at
        else:
            auto_updated_at_is_disabled = kwargs.pop('disable_auto_updated_at', False)
            if not auto_updated_at_is_disabled:
                self.updated_at = now()
        super(AutoCreatedUpdatedMixin, self).save(*args, **kwargs)


class SoftDeleteMixin(models.Model):

    deleted_at = models.DateTimeField(
        verbose_name=translate('deleted at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        kwargs = {
            'using': using,
        }
        if hasattr(self, 'updated_at'):
            kwargs['disable_auto_updated_at'] = True
        self.save(**kwargs)

class User(AbstractUser,AutoCreatedUpdatedMixin,SoftDeleteMixin):
    name = models.CharField(blank=False , max_length=30)

class Student(AutoCreatedUpdatedMixin,SoftDeleteMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hostel = models.CharField(max_length=100, blank=False , choices=HOSTEL_CHOICES)
    room = models.CharField(blank=False , max_length=10)
    contact = models.CharField(blank=False , max_length=10)
    roll = models.CharField(blank=False , max_length=10)