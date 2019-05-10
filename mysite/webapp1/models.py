from django.db import models
from django.utils import timezone
                                        # Create your models here.
class Login(models.Model):
    count=0
    username = models.CharField(max_length=200,primary_key=True)
    patient_id =   models.CharField(max_length=30,default='00000000')
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

class Address(models.Model):
    username=models.OneToOneField(Login,primary_key=True,on_delete=models.CASCADE)
    addressl1=models.CharField(max_length=60)
    addressl2=models.CharField(max_length=60)
    addcity=models.CharField(max_length=15)
    addstate=models.CharField(max_length=15)
    addzip=models.CharField(max_length=6)


class Medical1(models.Model):
    username=models.OneToOneField(Login,primary_key=True,on_delete=models.CASCADE)
    fever=models.CharField(max_length=9)
    highbp=models.CharField(max_length=9)
    lowbp=models.CharField(max_length=9)
    seizures=models.CharField(max_length=9)
    heart_d=models.CharField(max_length=9)
    fainting=models.CharField(max_length=9)
    diabetes=models.CharField(max_length=9)
    cholestrol=models.CharField(max_length=9)
    palp=models.CharField(max_length=9)                         
    otherdetail=models.CharField(max_length=500,default='----')
  
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
    date= models.DateField(default=timezone.now)


class Review(models.Model):
    count=0
    username = models.CharField(max_length=200)
    photo = models.CharField(max_length=50)
    review = models.CharField(max_length=100)
    rating = models.IntegerField(default=1)


class Doc_login(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=50,default='abc@gmail.com')

class Doc_profile(models.Model):
    username = models.OneToOneField(Doc_login,primary_key=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    gender=models.CharField(max_length=1)
    qualifications=models.CharField(max_length=200)
    mobile=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    photo=models.CharField(max_length=50)


class Doc_address(models.Model):
    username=models.OneToOneField(Doc_login,primary_key=True,on_delete=models.CASCADE)
    addressl1=models.CharField(max_length=60)
    addressl2=models.CharField(max_length=60)
    addcity=models.CharField(max_length=15)
    addstate=models.CharField(max_length=15)
    addzip=models.CharField(max_length=6)


class Report_sent(models.Model):
    count=0
    serial = models.IntegerField()
    doctor = models.CharField(max_length=200)
    patient = models.CharField(max_length=200)
    patient_id = models.CharField(max_length=30,default='00000000')
    reference_id = models.CharField(max_length=12)



class Conversation(models.Model):
    count=0
    serial = models.IntegerField(default=1)
    patient_id = models.CharField(max_length=30,default='00000000')
    patient = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    photo=models.CharField(max_length=50)
    msg = models.CharField(max_length=500)



