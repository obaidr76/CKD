from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Login
import os
import sklearn

# Create your views here.

def index(request):
    pass

def login(request):

    username = request.POST.get('username',False)
    password = request.POST.get('password',False)
    if username == False:
        template=loader.get_template('login.html')
        context=dict()
        return HttpResponse(template.render(context,request))
    else:
        logged = 0
        try:
            pas = Login.objects.get(pk=username)
            if pas.password == password:
                logged = 1
        except Login.DoesNotExist:
            logged = 0
        finally:
            context = {'logged': logged}
        if logged == 0:
            return render(request, 'login.html', context)
        else:
            return render(request, 'input.html', context)

def signup(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    email = request.POST.get('email', False)
    context = {'exist':0}
    if username == False:
        return HttpResponse('<h1>Page Error</h1>')
    else:
        try:
            pas = Login.objects.get(pk=username)
            exist = 1
            context['exist'] = exist
        except Login.DoesNotExist:
            l = Login(username,password,email)
            l.save()

        return render(request, 'login.html', context)


def input(request):
    context=dict()
    age = request.POST.get('age', False)
    albumin = request.POST.get('albumin', False)
    rbc = request.POST.get('rbc', False)
    bgr = request.POST.get('bgr', False)
    urea = request.POST.get('urea', False)
    createnine = request.POST.get('createnine', False)
    sodium = request.POST.get('sodium', False)
    potassium = request.POST.get('potassium', False)
    haemoglobin = request.POST.get('haemoglobin', False)
    hypertension = request.POST.get('hypertension', False)
    diabetes = request.POST.get('diabetes', False)
    wbcc = request.POST.get('wbcc', False)
    rbcc = request.POST.get('rbcc', False)
    if age == False:
        return HttpResponse('<h1>Page Error</h1>')
    else:
        #request = request.POST.map({'yes':1,'no':0,'normal':0,'abnormal':1})
        #hypertension = request.POST.get('hypertension', False)
        #diabetes = request.POST.get('diabetes', False)
        #rbc = request.POST.get('rbc', False)
        prediction = Classification([[age,albumin,rbc,bgr,urea,createnine,sodium,potassium,haemoglobin,wbcc,rbcc,hypertension,diabetes]])
        context['prediction'] = prediction
    return HttpResponse(prediction)

import pickle
def Classification(values,choice=1):
    scriptDirectory = os.path.dirname(os.path.realpath(__file__))
    choices = {0:'LogRegclassifier',1:'SVMclassifier',2:'DecisionTreeclassifier',3:'NBclassifier'}
    f = open(os.path.dirname(os.path.realpath(__file__))+'\\'+choices[choice],'rb')
    classifier = pickle.load(f)
    prediction = classifier.predict(values)
    f.close()
    if prediction ==0:
        return 'NoCKD'
    else:
        return 'CKD'


