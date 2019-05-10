from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Login,Profile, Reports, Review, Address, Medical1,Doc_login,Doc_profile,Doc_address,Report_sent, Conversation
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import sklearn
from .utils import render_to_pdf

# Create your views here.

def index(request):
    pass

def console(request,id='dprofile'):    
    context=dict()
    context['id']=id
    print('dprofile',id)
    if request.session.get('dusername',False)!=False:
        
        try:
            context['username']=request.session['dusername']
            ob1 = Doc_login.objects.get(pk=request.session.get('dusername',False))
            ob = Doc_profile.objects.get(pk=ob1)
            adr = Doc_address.objects.get(pk=ob1)
            context['prof']=ob.photo
            if id=='dprofile':
                
                context['name']=ob.name.strip()
                context['mobile']=ob.mobile.strip()
                context['gender']=ob.gender
                context['qualification']=ob.qualifications
                #print(type(ob.dob))
                #context['dob1']=str(ob.dob)
                context['email']=ob.email

                
                context['addressl1']=adr.addressl1
                context['addressl2']=adr.addressl2
                context['addcity']=adr.addcity
                context['addstate']=adr.addstate
                context['addzip']=adr.addzip
            if id =='dreport':
                ob_report_sent = Report_sent.objects.filter(doctor=request.session['dusername'])
                context['reports']=ob_report_sent
            if id == 'dcomms':
                ob_report_sent = Report_sent.objects.filter(doctor=request.session['dusername'])
                
                convo=set()
                convo_send=set()
                for conv in ob_report_sent:
                    if conv.patient_id in convo:
                        continue
                    convo.add(conv.patient_id)
                    ob_profile = Profile.objects.get(username=conv.patient)
                    conv.photo = ob_profile.photo
                    convo_send.add(conv)
                context['convo_send']=convo_send
            if id =='dchat':
                if request.method == 'GET':
                    patient_id = request.GET['patient_id']
                    doctor = request.session.get('dusername',False)
                    if doctor == False:
                        return HttpResponse("<h1>ERROR</h1>")
                    convos = Conversation.objects.filter(doctor=doctor,patient_id=patient_id).order_by("pk")
                    context['convos']=convos
                    context['patient_id']=patient_id
                    Login_ob = Login.objects.get(patient_id=patient_id)
                    context['patient']=Login_ob.username

 
                   

                
        except Doc_profile.DoesNotExist:
            pass
        template=loader.get_template('console.html')
        response  =  HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response
    else:
        
        return redirect(doc_login)

def home(request,id='index'):
    print('erw',id)
    context=dict()
    context['id']=id
    if id=='index':
        rev=Review.objects.all()
        context['rev']=rev
        for r in rev:
            r.rating = ['1']*r.rating
            r.rating.extend(['0']*(5-len(r.rating)))
    return render(request,'home.html',context)

def dashboard(request,id='1'):
    context=dict()
    print(id)
    context['id']=id
    if request.session.get('username',False)!=False:
        
        try:
            context['username']=request.session['username']
            ob1 = Login.objects.get(pk=request.session.get('username',False))
            ob = Profile.objects.get(pk=ob1)
            adr = Address.objects.get(pk=ob1)
            m1 = Medical1.objects.get(pk=ob1)
            context['prof']=ob.photo
            if id=='1':
                
                context['name']=ob.name.strip()
                context['mobile']=ob.mobile.strip()
                context['gender']=ob.gender
                context['dob']=ob.dob
                print(type(ob.dob))
                #context['dob1']=str(ob.dob)
                context['email']=ob.email

                
                context['addressl1']=adr.addressl1
                context['addressl2']=adr.addressl2
                context['addcity']=adr.addcity
                context['addstate']=adr.addstate
                context['addzip']=adr.addzip

                context['fever']=m1.fever
                context['lowbp']=m1.lowbp
                context['highbp']=m1.highbp
                context['seizures']=m1.seizures
                context['heart_d']=m1.heart_d
                context['fainting']=m1.fainting
                context['diabetes']=m1.diabetes
                context['cholestrol']=m1.cholestrol
                context['palp']=m1.palp
                context['otherdetail']=m1.otherdetail
                

            if id=='2':
                pass
                
            if id=='3':
                #print(request.GET['reference_id'])
                report = Reports.objects.get(reference_id = request.GET['reference_id'])
                pred = report.stage
                prediction = 'CKD' if report.pred else 'NoCKD'
                egfr = report.egfr
                albumin = report.albumin
                diab = 1 if report.diabetes else 0
                bgr = report.bgr
                haemoglobin = report.haemoglobin
                date1=report.date
                reference_id=request.GET['reference_id']
                
                patient_id=report.patient_id
                context =dict()
                context['pred']=pred
                context['egfr']=egfr
                context['albumin']=albumin
                context['id']='3'
                context['diab']=bgr
                context['haem']=haemoglobin
                context['prediction']=prediction
                context['date']=date1
                context['reference_id']=reference_id
                context['username']=request.session['username']
                context['patient_id']=patient_id
                print(context)


            if id=='4':
                context['prof']=ob.photo
                rev = Review.objects.all()
                for r in rev:
                    r.rating = ['1']*r.rating
                    r.rating.extend(['0']*(5-len(r.rating)))
                context['rev']=rev
                

            if id=='5':
                print('dsfh')
                doc_ob = Doc_profile.objects.all()
                patient_id = Login.objects.get(pk=request.session['username']).patient_id
                reports = list(Reports.objects.filter(patient_id=patient_id))
                print('reports',reports)
                for report in reports:
                    print(report.pred)
                    report.pred = 'CKD' if report.pred else 'NoCKD'
                    print(report.pred)
                context['doctors']=doc_ob
                context['reports']=reports
                context['i']='0'
                context['patient_id']=ob1.patient_id
            if id == '6':
                context['gender']=ob.gender

            if id=='7':
                convo_pat = Report_sent.objects.filter(patient=request.session.get('username',False))
                for each in convo_pat:
                    doctor = each.doctor
                    ob_doc_prof = Doc_profile.objects.get(username=doctor)
                    each.photo = ob_doc_prof.photo
                context['conversation']=convo_pat  
            
            if id=='8':
                if request.method == 'GET':
                    patient_id = request.GET['patient_id']
                    doctor = request.GET['doctor']
                    patient = request.session.get('username',False)
                    if doctor == False:
                        return HttpResponse("<h1>ERROR</h1>")
                    convos = Conversation.objects.filter(doctor=doctor,patient_id=patient_id).order_by("pk")
                    context['convos']=convos
                    context['patient_id']=patient_id
                    context['patient']=patient
                    context['doctor']=doctor
                    #ob_dprofile = Doc_profile.objects.get(username=doctor)
                    #context['photo']=ob_dprofile.photo
            
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
            id=1
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
            p=Profile(username,'','','1871-06-06','','','')
            p.save()

            a=Address(username,'','','','','')
            a.save()

            m=Medical1(username,'unchecked','unchecked','unchecked','unchecked','unchecked','unchecked','unchecked','unchecked','unchecked','')
            m.save()

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
        albumin = float(request.POST.get('albumin', False))
        rbc = float(request.POST.get('rbc', False))
        bgr = request.POST.get('bgr', False)
        urea = request.POST.get('urea', False)
        createnine = float(request.POST.get('createnine', False))
        sodium = request.POST.get('sodium', False)
        potassium = request.POST.get('potassium', False)
        haemoglobin = request.POST.get('haemoglobin', False)
        hypertension = float(request.POST.get('hypertension', False))
        diabetes = float(request.POST.get('diabetes', False))
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
            age = int(age)**(-0.203)
            createnine = 186*((float(createnine)*100/6)/88.4)**(-1.154)
            egfr = age*createnine*cost
            Acr=albumin/createnine
            #egfr=90
            #Acr=30

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
            date1=today
    else:
        reference_id=request.GET['reference_id']
        '''report = Reports.objects.get(reference_id = request.GET['reference_id'])
        pred = report.stage
        prediction = 'CKD' if report.pred else 'NoCKD'
        egfr = report.egfr
        albumin = report.albumin
        diab = 1 if report.diabetes else 0
        bgr = report.bgr
        haemoglobin = report.haemoglobin
        date1=report.date
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
    context['date']=date1
    context['reference_id']=reference_id
    context['username']=request.session['username']
    context['patient_id']=patient_id'''
    
    return redirect('../dashboard/3/?reference_id='+reference_id,request)
import pickle
def Classification(values,choice=1):
    scriptDirectory = os.path.dirname(os.path.realpath(__file__))
    choices = {0:'LogRegclassifier',1:'SVMclassifier',2:'DecisionTreeclassifier',3:'NBclassifier'}
    f = open(os.path.dirname(os.path.realpath(__file__))+'\\'+choices[choice],'rb')
    classifier = pickle.load(f)
    f1 = open(os.path.dirname(os.path.realpath(__file__))+'\\'+'ScalarObject','rb')
    scalar = pickle.load(f1)
    
    values = scalar.transform(values)
    prediction = classifier.predict(values)
    f.close()
    if prediction ==0:
        return 'NoCKD'
    else:
        return 'CKD'


def logout(request):
    if request.session.get('username',False)!=False:
        del request.session['username']
    if request.session.get('dusername',False)!=False:
        del request.session['dusername']
    request.session['justlogout']=1
    return redirect('home')


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
        return redirect('dashboard1')





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
        try:
            return render(request,'download.html', context)
        except:
            pass
        #pdf = render_to_pdf(response)
        '''if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            #filename = "report_%s.pdf" %("12341231")
            #content = "inline; filename='%s'" %(filename)
            ##download = request.GET.get("download")
            #if download:
            #content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content'''
        #return response
        #return HttpResponse("Not found")
        #return HttpResponse(pdf, content_type='application/pdf')

def review(request):
    text = request.POST['text']
    username = request.session['username']
    prof = request.POST['prof']
    rating =request.POST['rating'] 
    print(rating)
    Review.count+=1
    rev = Review(Review.count,username,prof,text,rating)
    rev.save()
    return HttpResponse("<h1>fbjhfjch</h1>")

def address(request):     
    username = request.session['username']                                                  #address
    addressl1 = request.POST.get('addressl1','')
    addressl2 = request.POST.get('addressl2','')
    addcity = request.POST.get('addcity','')
    addstate = request.POST.get('addstate','')
    addzip = request.POST.get('addzip','')
    address_save = Address(username,addressl1,addressl2,addcity,addstate,addzip)
    address_save.save()
    return redirect('dashboard1')

def medical1(request):
    username = request.session['username']                                                  #address
    fever = request.POST.get('fever','unchecked')
    highbp = request.POST.get('highbp','unchecked')
    lowbp = request.POST.get('lowbp','unchecked')
    seizures = request.POST.get('seizures','unchecked')
    heart_d = request.POST.get('heart_d','unchecked')
    fainting = request.POST.get('fainting','unchecked')
    diabetes = request.POST.get('diabetes','unchecked')
    cholesterol = request.POST.get('cholesterol','unchecked')
    palp = request.POST.get('palp','unchecked')
    otherdetail = request.POST.get('otherdetail','fuck')
    medical1_save = Medical1(username,fever,highbp,lowbp,seizures,heart_d,fainting,diabetes,cholesterol,palp,otherdetail)
    medical1_save.save()
    return redirect('dashboard1')


def doc_profile(request):
    context=dict()
    if request.POST.get('name',False)!=False:
        name=request.POST.get('name','')        
        gender=request.POST.get('gender','')
        qualifications=request.POST.get('qualification','')
        #print(dob)
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
            ob=Doc_login.objects.get(pk=request.session['dusername'])
            ob1 = Doc_profile.objects.get(pk=ob)
            if qualifications=='':
                qualifications=ob1.qualifications
            if url=='':
                url=ob1.photo    
                print(url)
            ob1.name=name
            ob1.gender=gender
            ob1.qualifications=qualifications
            ob1.mobile=mobile
            ob1.photo=url
            ob1.email=email
            ob1.save()
        except Doc_profile.DoesNotExist:
            prof=Doc_profile(request.session['dusername'],name,gender,qualification,mobile,email,url)
            prof.save()
        #finally:
        context['name']=name
        context['gender']=gender
        context['qualification']=qualifications
        context['email']=email
        context['mobile']=mobile
        context['prof'] = url
        context['id']='dprofile'
        id='dprofile'
        return redirect('console',id)


def doc_address(request):
    username = request.session['dusername']                                                  #address
    addressl1 = request.POST.get('addressl1','')
    addressl2 = request.POST.get('addressl2','')
    addcity = request.POST.get('addcity','')
    addstate = request.POST.get('addstate','')
    addzip = request.POST.get('addzip','')
    address_save = Doc_address(username,addressl1,addressl2,addcity,addstate,addzip)
    address_save.save()
    return redirect('console')


def doc_login(request):
    context=dict()
    username = request.POST.get('username',False)
    password = request.POST.get('password',False)
    if username == False and request.session.get('notlogged',False)!=False and request.session.get('justlogout',False)==False:
        context['notlogged']= request.session['notlogged']
        del request.session['notlogged']
        template=loader.get_template('doc_login.html')
        response = HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response
    if request.session.get('justlogout',False)!=False:
        del request.session['justlogout']
    if request.session.get('dusername',False) != False:
        return redirect('console')
    
    if username == False:
        template=loader.get_template('doc_login.html')
        response= HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response
    else:
        logged = 0
        request.session['dusername']=False
        try:
            pas = Doc_login.objects.get(pk=username)
            if pas.password == password:
                logged = 1
                request.session['dusername']=False
        except Doc_login.DoesNotExist:
            pass
        #finally:
        context['logged']=logged
        if logged == 0:
            template=loader.get_template('doc_login.html')
            response= HttpResponse(template.render(context,request))
            response['Cache-Control']='no-store'
            return response
        else:
            id='dprofile'
            request.session['dusername']=username
            return redirect('console',id)




def doc_signup(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    email = request.POST.get('email', False)
    context = {'exist':0}
    if username == False:
        return HttpResponse('<h1>Page Error</h1>')
    else:
        try:
            pas = Doc_login.objects.get(pk=username)
            exist = 1
            context['exist'] = exist
        except Doc_login.DoesNotExist:
            
            l = Doc_login(username,password,email)
            l.save()
            p=Doc_profile(username,'','','','','','')
            p.save()

            a=Doc_address(username,'','','','','')
            a.save()

           

        template=loader.get_template('doc_login.html')
        response= HttpResponse(template.render(context,request))
        response['Cache-Control']='no-store'
        return response


def report_sent(request):
    patient = request.POST['username']
    doctor = request.POST['doctor']
    patient_id=request.POST['patient_id']
    reference_id=request.POST['reference_id']
    try:
        ob= Report_sent.objects.get(reference_id=reference_id)
    #print(rating)
    except Report_sent.DoesnotExist:
        print(Report_sent.count)
        Report_sent.count+=1
        Report_sent.count
        rev = Report_sent(Report_sent.count,Report_sent.count,doctor,patient,patient_id,reference_id)
        rev.save()
    
    return HttpResponse("<h1>fbjhfjch</h1>")


def consultation(request):
    
    msg = request.POST['msg']
    doctor = request.POST['doctor']
    patient = request.POST['patient']
    patient_id = request.POST['patient_id']
    photo = request.POST['photo']
    print(Conversation.count)
    Conversation.count += 1
    print(Conversation.count)
    rev = Conversation(Conversation.count,Conversation.count,patient_id,patient,doctor,photo,msg)
    rev.save()
    return HttpResponse("<h1>fbjhfjch</h1>")