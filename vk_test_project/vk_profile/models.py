from django.db import models
from django.contrib.auth.models import User


class FirstVisit(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
