from django.db import models

# Create your models here.
class Login(models.Model):
    count=0
    username = models.CharField(max_length=200,primary_key=True)
    patient_id =   models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50,default='abc@gmail.com')
    objects = models.Manager()
    DoesNotExist = models.ObjectDoesNotExist

class Profile(models.Model):
    username=models.OneToOneField(Login,primary_key=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    gender=models.CharField(max_length=1)
    dob=models.DateField()
    mobile=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    photo=models.CharField(max_length=50)

class Reports(models.Model):
    count=0
    reference_id = models.CharField(max_length=12,primary_key=True)
    patient_id =  models.CharField(max_length=30)
    #models.ForeignKey(Login,on_delete = 'CASCADE')
    age  = models.IntegerField()
    albumin =models.DecimalField(decimal_places = 4,max_digits = 9)
    rbc = 	models.BooleanField()
    bgr = models.DecimalField(decimal_places = 4,max_digits = 9)
    bu = models.DecimalField(decimal_places = 4,max_digits = 9)
    createnine = models.DecimalField(decimal_places = 4,max_digits = 9)
    sodium = models.DecimalField(decimal_places = 4,max_digits = 9)
    patassium=models.DecimalField(decimal_places = 4,max_digits = 9)
    haemoglobin = models.DecimalField(decimal_places = 4,max_digits = 9)
    wbcc =models.DecimalField(decimal_places = 4,max_digits = 9)
    rbcc =models.DecimalField(decimal_places = 4,max_digits = 9)
    hypertension =	models.BooleanField()
    diabetes = 	models.BooleanField()
    egfr = models.DecimalField(decimal_places = 4,max_digits = 9)
    acr = models.DecimalField(decimal_places = 4,max_digits = 9)
    pred = 	models.BooleanField()
    stage = models.CharField(max_length=5)