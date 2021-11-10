from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from random import choice
import string


class Urls(models.Model):
    url_long=models.URLField()
    url_short=models.URLField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


# Create your models here.
