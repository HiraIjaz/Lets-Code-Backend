from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    TYPE_CHOICES = (
        ("mcq", "MCQ"),
        ("coding", "Coding"),
    )
    title = models.TextField(help_text="title or description of the question")
    # The 'data' field stores JSON data representing the question details.
    data = models.JSONField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="mcq")
    isDeleted = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.title
