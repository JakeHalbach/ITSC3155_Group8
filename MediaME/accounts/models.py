from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True)
    genres = models.TextField(blank=True)
    media_types = models.TextField(blank=True)
    favorite_titles = models.TextField(blank=True)
    interaction_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"
=======

# Create your models here.
>>>>>>> JakeHalbach
