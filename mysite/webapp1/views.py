from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Login,Profile, Reports, Review
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import sklearn
from .utils import render_to_pdf

# Create your views here.

def index(request):
    pass

def dashboard(request,id=1):
    context=dict()
    context['id']=id
    if request.session.get('username',False)!=False:
        try:
            context['username']=request.session['username']
            ob1 = Login.objects.get(pk=request.session.get('username',False))
            ob = Profile.objects.get(pk=ob1)
            context['prof']=ob.photo
            if id=='1':
                
                context['name']=ob.name
                context['mobile']=ob.mobile
                context['gender']=ob.gender
                context['dob']=ob.dob
                #print(type(ob.dob))
                #context['dob1']=str(ob.dob)
                context['email']=ob.email
                
            if id=='2':
                pass
                
            if id=='3':
                pass
            if id=='4':
                context['prof']=ob.photo
                rev = Review.objects.all()
                context['rev']=rev
                

            if id=='5':
                print('dsfh')
                
                patient_id = Login.objects.get(pk=request.session['username']).patient_id
                reports = list(Reports.objects.filter(patient_id=patient_id))
                print('reports',reports)
                for report in reports:
                    print(report.pred)
                    report.pred = 'CKD' if report.pred else 'NoCKD'
                    print(report.pred)
                context['reports']=reports
                context['i']='0'
                context['patient_id']=ob1.patient_id
            if id == '6':
                pass
                
            
            
            
            #exists
        except Profile.DoesNotExist:
            pass
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
            patient_id = 'PID000'
            Login.count+=1
            length = len(str(Login.count))
            add = '0'*(3-length)
            patient_id += add+str(Login.count)
            l = Login(username,patient_id,password,email)
            l.save()

        template=loader.get_template('login.html')
        response= HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response


def input(request):
    context=dict()
    prof=''
    ob1=Profile.objects.get(pk=request.session['username'])
    prof=ob1.photo
    if request.method =="POST":
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
            gender='f'
            if gender=='f':
                cost=0.742
            else:
                cost=1
            #age = int(age)**(-0.203)
            #createnine = 186*((float(createnine)*100/6)/88.4)**(-1.154)
            #gfr = age*createnine*cost
            #Acr=albumin/createnine
            egfr=90
            Acr=30

            pred=''
            if egfr>=90:
                pred+='g1'
            elif egfr>=60:
                pred+='g2'
            elif egfr>=45:
                pred+='g3a'
            elif egfr>=30:
                pred+='g3b'
            elif egfr>=15:
                pred+='g4'
            else:
                pred+='g5'

            if Acr<30:
                pred+='a1'
            elif Acr<=300:
                pred+='a2'
            else:
                pred+='a3'
            ob = Login.objects.get(pk=request.session['username'])
            patient_id = ob.patient_id
            
            print(patient_id)
            Reports.count += 1
            today = str(date.today().day)+str(date.today().month)+str(date.today().year)
            reference_id = patient_id[6:]+today+str(Reports.count)
            dia = True if diabetes=='1' else False
            Rbc = True if rbc=='1' else False
            hyp = True if hypertension=='1' else False
            pre = True if prediction=='CKD' else False
            print('createnihn',createnine)
            report = Reports(reference_id,patient_id,int(age),float(albumin),Rbc,float(bgr),float(urea),float(createnine),float(sodium),float(potassium),float(haemoglobin),float(wbcc),float(rbcc),hyp,dia,float(egfr),float(Acr),pre,pred)
            report.save()
    else:
        report = Reports.objects.get(reference_id = request.GET['reference_id'])
        pred = report.stage
        prediction = 'CKD' if report.pred else 'NoCKD'
        egfr = report.egfr
        albumin = report.albumin
        diab = 1 if report.diabetes else 0
        bgr = report.bgr
        haemoglobin = report.haemoglobin
        date=report.date
        reference_id=request.GET['reference_id']
        patient_id=report.patient_id
    context =dict()
    context['pred']=pred
    context['id']='3'
    context['egfr']=egfr
    context['albumin']=albumin
    context['diab']=bgr
    context['haem']=haemoglobin
    context['prediction']=prediction
    context['prof']=prof
    context['date']=date
    context['reference_id']=reference_id
    context['username']=request.session['username']
    context['patient_id']=patient_id
    return render(request,'dashboard.html',context)

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





def download(request):
    if request.method=="GET":
        report = Reports.objects.get(reference_id = request.GET['reference_id'])
        context=dict()
        context['pred']=report.stage
        context['egfr']=report.egfr
        context['albumin']=report.albumin
        context['diab']=report.bgr
        context['haem']=report.haemoglobin
        context['reference_id'] = request.GET['reference_id']
        context['date']=report.date
        context['username']=request.session['username']
        context['patient_id']=report.patient_id
        #return render(request,'download.html',context)
        response = render('download.html', context)
        pdf = render_to_pdf(response)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "report_%s.pdf" %("12341231")
            #content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        #return HttpResponse(pdf, content_type='application/pdf')







def review(request):
    text = request.POST['text']
    username = request.session['username']
    prof = request.POST['prof']
    rating =5 
    Review.count+=1
    rev = Review(Review.count,username,prof,text,rating)
    rev.save()
    return HttpResponse("<h1>fbjhfjch</h1>")
