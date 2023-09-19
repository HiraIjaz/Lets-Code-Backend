from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.TextField()
    data = models.JSONField()
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.title

