from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    name = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField('Post', related_name='posts', through='PostTags')


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    content = models.TextField()
    owner = models.ForeignKey('auth.user', related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, through='PostTags')


class PostTags(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
