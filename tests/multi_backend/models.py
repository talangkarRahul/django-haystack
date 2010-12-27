from django.db import models

class Post(models.Model):
    lang = models.CharField(max_length=2)
    title = models.CharField(max_length=50)
    body = models.TextField()