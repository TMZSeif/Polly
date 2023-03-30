from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Options(models.Model):
    name = models.CharField(max_length=100)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    votes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class MyUser(AbstractUser):
    options = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, default=None)

class Poll(models.Model):
    question = models.CharField(max_length=100)
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)
    def __str__(self):
        return self.question