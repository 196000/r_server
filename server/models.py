from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    file = models.FileField(upload_to = 'server/')
    #md5 = models.CharField(max_length=32)
