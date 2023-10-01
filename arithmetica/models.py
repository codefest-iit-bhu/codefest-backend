from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class UserInfo(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE)
    credits=models.FloatField(default=30.0,validators=[
            MinValueValidator(0)
        ])
    lives=models.IntegerField(default=3,validators=[
            MinValueValidator(0)])

    def __str__(self):
        return f"{self.user} with id {self.user.id}"

class RoundInfo(models.Model):
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    problem_statement=models.TextField()

    def __str__(self):
        return f"{self.problem_statement[:50]} with id {self.id}"

class ErrorInfo(models.Model):
    user_info=models.ForeignKey(to=UserInfo,on_delete=models.CASCADE)
    round=models.ForeignKey(to=RoundInfo,on_delete=models.CASCADE)
    error=models.FloatField(default=30.0,validators=[
            MinValueValidator(0)
        ])
    submitted_function=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    credits=models.FloatField(default=30.0,validators=[
            MinValueValidator(0)
        ])

    class Meta:
        unique_together=('user_info','round')

    def __str__(self):
        return f"{self.user_info.user} in round {self.round.id}"
