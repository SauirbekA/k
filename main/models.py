from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from django.conf import settings
from django.contrib.auth.models import User, Group
from tinymce.models import HTMLField

class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/courses', blank=True, default='default/anonymous-user.png')
    price = models.FloatField()
    idUser = models.IntegerField(null=True)
    video = models.FileField(upload_to='video/course', blank=True)
    is_published = models.BooleanField(null=True, default=False)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('coursepage', kwargs={'id': self.pk})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

class Video(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    idCourse = models.IntegerField()
    url = EmbedVideoField()
    # video = models.FileField(upload_to='video/lessons', blank=True)
    # content = HTMLField(blank=True, default="")
    # notes = HTMLField(blank=True, default="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('create_lesson', kwargs={'id': self.pk})    


class LessonContainer(models.Model):
    idUser = models.IntegerField()
    idCourse = models.IntegerField()

class Learner(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='photos/users/', blank=True, default='default/anonymous-user.png')    
    phone = models.CharField(max_length=20, null=True)

class Cart(models.Model):
    idUser = models.IntegerField()
    idCourse = models.IntegerField()

from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id', 'email']
