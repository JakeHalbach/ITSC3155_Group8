from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Creator(models.Model):
    name = models.CharField(max_length=200)
    #medias = 

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Media(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(Creator, on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, related_name='media_items', blank=True)
    media_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    # poster = models.ImageField(upload_to='media_posters/')
    ##tags= 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    media_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    ##poster = models.ImageField()
    ##poster = models.ImageField()

    def __str__(self):
        return self.title


class Room(models.Model):
    TABS = [
        ('reviews', 'Reviews'),
        ('characters', 'Characters'),
        ('plot', 'Plot'),
        ('visuals', 'Visuals'),
    ]
    
    
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    media = models.ForeignKey(Media, related_name="rooms", on_delete=models.SET_NULL, null=True, blank=True)
    tab = models.CharField(max_length=20, choices=TABS)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.media:
            self.name = self.media.title
        super(Room, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.content[0:50]



# Create your models here.

#env/scripts/activate
#cd mediame
#python manage.py makemigrations
