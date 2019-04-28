from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Login,Profile
from django.core.files.storage import FileSystemStorage
import os
import sklearn

# Create your views here.

def index(request):
    pass

def dashboard(request,id=1):
    context=dict()
    context['id']=id
    if request.session.get('username',False)!=False:
        try:
            ob1 = Login.objects.get(pk=request.session.get('username',False))
            ob = Profile.objects.get(pk=ob1)
            context['name']=ob.name
            context['mobile']=ob.mobile
            context['gender']=ob.gender
            context['dob']=ob.dob
            #print(type(ob.dob))
            #context['dob1']=str(ob.dob)
            context['email']=ob.email
            context['prof']=ob.photo
            #exists
        except Profile.DoesNotExist:
            pass
        finally:
            template=loader.get_template('dashboard.html')
            response  =  HttpResponse(template.render(context,request))
            response['Cache-Control']='no-store'
            return response
    else:
        context['notlogged']=1
        request.session['notlogged']=1
        return redirect('login')

def login(request):
    context=dict()
    username = request.POST.get('username',False)
    password = request.POST.get('password',False)
    if username == False and request.session.get('notlogged',False)!=False and request.session.get('justlogout',False)==False:
        context['notlogged']= request.session['notlogged']
        del request.session['notlogged']
        template=loader.get_template('login.html')
        response = HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response
    if request.session.get('justlogout',False)!=False:
        del request.session['justlogout']
    if request.session.get('username',False) != False:
        return redirect('dashboard1')
    
    if username == False:
        template=loader.get_template('login.html')
        response= HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response
    else:
        logged = 0
        request.session['username']=False
        try:
            pas = Login.objects.get(pk=username)
            if pas.password == password:
                logged = 1
                request.session['username']=False
        except Login.DoesNotExist:
            pass
        #finally:
        context['logged']=logged
        if logged == 0:
            template=loader.get_template('login.html')
            response= HttpResponse(template.render(context,request))
            response['Cache-Control']='no-store'
            return response
        else:
            id=2
            request.session['username']=username
            return redirect('dashboard',id)

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

        template=loader.get_template('login.html')
        response= HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response


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


def logout(request):
    if request.session.get('username',False)!=False:
        del request.session['username']
    request.session['justlogout']=1
    return redirect('login')


def profile(request):
    context=dict()
    if request.POST.get('name',False)!=False:
        name=request.POST.get('name','')        
        gender=request.POST.get('gender','')
        dob=request.POST.get('dob','')
        print(dob)
        '''if dob!='':
            date = dob.split('-')
            dob = date[2]+'-'+date[1]+'-'+date[0]'''
        mobile=request.POST.get('mobile','')
        email=request.POST.get('email','')
        if request.FILES:
            photo=request.FILES['photo']
            fs=FileSystemStorage()
            pname=fs.save(photo.name,photo)
            url=fs.url(pname)
        else:
            url=''
            
        try:
            ob=Login.objects.get(pk=request.session['username'])
            ob1 = Profile.objects.get(pk=ob)
            if dob=='':
                dob=ob1.dob
            if url=='':
                url=ob1.photo    
                print(url)
            ob1.name=name
            ob1.gender=gender
            ob1.dob=dob
            ob1.mobile=mobile
            ob1.photo=url
            ob1.email=email
            ob1.save()
        except Profile.DoesNotExist:
            prof=Profile(request.session['username'],name,gender,dob,mobile,email,url)
            prof.save()
        #finally:
        context['name']=name
        context['gender']=gender
        context['dob']=dob
        context['email']=email
        context['mobile']=mobile
        context['prof'] = url
        context['id']='1'
        return render(request,'dashboard.html',context)