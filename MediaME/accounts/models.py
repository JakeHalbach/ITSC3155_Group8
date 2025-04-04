from django.db import models
from django.contrib.auth.models import User
from base.models import Type, Media, Genre

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    media_types = models.ManyToManyField(Type, blank=True)
    favorite_titles = models.ManyToManyField(
        Media, related_name='favorites', blank=True)
    interaction_score = models.IntegerField(default=0)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
