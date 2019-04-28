from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50,default='abc@gmail.com')
    objects = models.Manager()
    DoesNotExist = models.ObjectDoesNotExist

class Profile(models.Model):
    username=models.OneToOneField('Login',primary_key=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    gender=models.CharField(max_length=1)
    dob=models.DateField()
    mobile=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    photo=models.CharField(max_length=50)