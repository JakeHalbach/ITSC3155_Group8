from django.db import models
from django.contrib.auth.models import User
from base.models import Type, media

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    genres = models.TextField(blank=True)
    Type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    favorite_titles = models.ManyToManyField(
        media, related_name='favorites', blank=True)
    interaction_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"
