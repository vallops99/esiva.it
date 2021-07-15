from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save, post_delete
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
@receiver(post_delete, sender=Location)
def location_post_save(sender, instance, **kwargs):
    locations_key = 'esiva.it/locations'
    road_key = 'esiva.it/roads'
    live_point_key = 'esiva.it/live-point'
    caches['context-processor'].delete_many([
        locations_key,
        road_key,
        live_point_key
    ])


class Message(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True)

    user = models.CharField(max_length=50, blank=True, null=True)

    age = models.IntegerField(blank=True, null=True)

    is_reviewed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.user

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, **kwargs):
    caches['context-processor'].clear()
    caches['default'].clear()


class JournalArticle(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)

    content = RichTextField(blank=True, null=True)

    image = models.ImageField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title

@receiver(post_save, sender=JournalArticle)
def journal_article_post_save(sender, instance, **kwargs):
    caches['context-processor'].clear()
    caches['default'].clear()


class Audio(models.Model):
    file = models.FileField(blank=True, null=True)

    downloaded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class YoutubeVideo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    video_id = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title;

@receiver(post_save, sender=YoutubeVideo)
def youtube_video_post_save(sender, instance, **kwargs):
    caches['context-processor'].clear()
    caches['default'].clear()
