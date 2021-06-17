from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import caches
import datetime

class Location(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    coordinate_x = models.FloatField(null=True, blank=True)
    coordinate_y = models.FloatField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    is_city = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Location)
def location_post_save(sender, instance, **kwargs):
    caches['context-processor'].clear()

class Message(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)

    kind_of = models.CharField(max_length=6, choices=[
        ('planet', 'planet'),
        ('bok', 'bok')
    ], default='bok')

    user = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)

    is_reviewed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, **kwargs):
    caches['context-processor'].clear()
