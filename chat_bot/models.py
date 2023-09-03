from django.db import models


# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True)
