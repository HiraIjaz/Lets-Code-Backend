from django.db import models
from django.contrib.auth.models import User
from questions.models import Question


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name='assignemt')


    objects = models.Manager()

    def __str__(self):
        return self.title


class AssignmentEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.user} enrolled in {self.assignment}'

