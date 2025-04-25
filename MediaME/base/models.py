from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Media(models.Model):
    title = models.CharField(max_length=200)
    creators = models.ManyToManyField(Creator, related_name='created_media', blank=True)
    genres = genres = models.ManyToManyField(Genre, related_name='media_items', blank=True)
    media_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    poster = models.ImageField(upload_to='images/', null=True, blank=True, default='../images/images/spongeboy.jpg')
    favorited = models.ManyToManyField(User, related_name='favorite_media', blank=True)
    
    def poster_url(self):
        if self.poster and hasattr(self.poster, 'url'):
            return self.poster.url
        
    def is_favorited(self, user):
        return self.favorited.filter(id=user.id).exists()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.rooms.exists():
            for tab in ['reviews', 'characters', 'plot', 'visuals']:
                Room.objects.create(media=self, tab=tab)

    class Meta:
        ordering = ['-updated', '-created']

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
        if self.media and self.tab:
            self.name = f"{self.media.title} - {self.tab.capitalize()}"
        super().save(*args, **kwargs)

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



#env/scripts/activate
#cd mediame
#python manage.py makemigrations
