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

class Media(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(Creator, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    ##tags= 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    media_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Create your models here.

#env/scripts/activate
#cd mediame
#python manage.py makemigrations
