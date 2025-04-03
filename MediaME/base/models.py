from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class creator(models.Model):
    name = models.CharField(max_length=200)
    #medias = 

    def __str__(self):
        return self.name

class media(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(creator, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    ##tags= 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
# Create your models here.

#env/scripts/activate
#cd mediame
#python manage.py makemigrations
