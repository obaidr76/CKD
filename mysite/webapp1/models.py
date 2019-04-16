from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50,default='abc@gmail.com')
    objects = models.Manager()
    DoesNotExist = models.ObjectDoesNotExist