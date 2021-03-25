from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)