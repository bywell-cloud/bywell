from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , get_object_or_404
from django.urls import reverse
import datetime
from django.core.serializers import serialize
from django.core import serializers
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#from rest_framework import generics

from django import forms
from django.http import JsonResponse

from datetime import timedelta ,datetime ,date
#from .serializer import TaskSerializer#

from .models import User , Projects , Task , Comments



class DateInput(forms.DateInput):
    input_type = 'date'

class DateInput1(forms.DateInput):
    input_type = 'date'


class Createlevel(forms.ModelForm):
    
    #userlevels = forms.CharField(max_length=50, required = True)

    class Meta:
        model = User
        

        fields =[
                  'userlevels' 
                  ]

        

        labels = {
            'userlevels': 'Role' 
        }

       

     
class Assign(forms.ModelForm):
    
    name = forms.CharField(label ='', max_length=200, required = True,widget=forms.TextInput(attrs={'placeholder':'Enter Task Name here ..' , 'class':'form-control'}))
    t_description= forms.CharField(label=' ' ,max_length=1000,
                           widget= forms.Textarea
                           (attrs={'placeholder':'Enter your Description here ....', 'class': 'form-control', 'cols': 30 , 'rows':5}))  
    class Meta:
        model = Task
        expected_end = forms.DateField(widget=DateInput())
        start_time = forms.DateField(widget=DateInput1())
        fields =[
                  'name',
                  't_description' ,
                  'asignedto',
                  'start_time',
                  'expected_end'
                  ]

        widgets = {
            'expected_end': DateInput(attrs={'class':'form-control'}),
            'start_time': DateInput1(attrs={'class':'form-control'})
        }
       

        labels = {
            't_description': '' ,'name':'' , 'asignedto':'Assigned To' , 'expected_end':'Expected End Date','start_time':'Start Date'
        }

class Task2(forms.ModelForm):

    tchoice =(
    (0,  "0%") ,   
    (10, "1 to 10%"), 
    (20, "11 to 20%"), 
    (30, "21 to 30%"), 
    (40, "31 to 40%"), 
    (50, "41 to 50%"),
    (60, "51 to 60%"),
    (70, "61 to 70%"),
    (80, "71 to 80%"),
    (90, "81 to 90%"),
    (99, "91 to 99%") ,
    (100,"Completed")

)
  
    status = forms.ChoiceField(choices = tchoice)   
    name = forms.CharField(label ='', max_length=200, required = True,widget=forms.TextInput(attrs={ 'class':'form-control'}))
    t_description= forms.CharField(label=' ' ,max_length=1000,
                           widget= forms.Textarea
                           (attrs={'class': 'form-control', 'cols': 30 , 'rows':5}))  
    class Meta:
        model = Task
        expected_end = forms.DateField(widget=DateInput())
        start_time = forms.DateField(widget=DateInput1())
        fields =[
                  'name',
                  't_description' ,
                  'asignedto',
                  'start_time',
                  'expected_end',
                  'status'
                  ]

        widgets = {
            'expected_end': DateInput(attrs={'class':'form-control'}),
            'start_time': DateInput1(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'})
        }
       

        labels = {
            't_description': '' ,'name':'' , 'asignedto':'Assigned To' , 'expected_end':'Expected End Date','start_time':'Start Date'
        }        



    
class Progress(forms.ModelForm): 
    tchoice =(
    (0,  "0%") ,   
    (10, "1 to 10%"), 
    (20, "11 to 20%"), 
    (30, "21 to 30%"), 
    (40, "31 to 40%"), 
    (50, "41 to 50%"),
    (60, "51 to 60%"),
    (70, "61 to 70%"),
    (80, "71 to 80%"),
    (90, "81 to 90%"),
    (99, "91 to 99%") ,
    (100,"Completed")
)
  
    status = forms.ChoiceField(choices = tchoice )
    widgets = {

        'status':forms.Select(attrs={'class':'form-control'})  
    }
    
   
    class Meta:
        model = Task
        
        fields =[
                  'status'
                  ]

        



class AddProject(forms.ModelForm):
    name = forms.CharField(label ='', max_length=200, required = True,widget=forms.TextInput(attrs={'placeholder':'Enter Project Name here ..' , 'class':'form-control'}))
   
    status2 = forms.BooleanField( widget=forms.HiddenInput(), required = False)
    status = forms.IntegerField( widget=forms.HiddenInput(), required = False)
    completed = forms.IntegerField(label='completed', widget=forms.HiddenInput() ,required = False)
    not_completed = forms.IntegerField(label='not_completed', widget=forms.HiddenInput() , required = False)
    class Meta:
        model = Projects
       
        fields =['name'
                  ]

        
        labels = {
            'name': '' 
        }

       

        #exclude ={ 'status' }

def index(request):
    if not request.user.is_authenticated:
        
        return render(request, 'prjtask/login.html' ) 
    else:    
        user0 =  User.objects.get(username=request.user.username)
        prj = Projects.objects.all()
        tsk = Task.objects.all()
        if user0.userlevels == 1:
            rolelevel = 1
            
        else:
            rolelevel= 2
            user00 = User.objects.get(username=request.user.username)
            userall= User.objects.all()
            tsk0 = Task.objects.filter(asignedto_id=user00.id).order_by('-start_time')
            otsk0 = Task.objects.filter(asignedto_id=user00.id).values('project_id').distinct()
           
            
            prjtsk = Projects.objects.all()         
            
            return  render(request,"prjtask/index.html",{'rolelevel':rolelevel ,'task0':tsk0,'user00':userall  , 'prjtsk':prjtsk ,'prj1':prj ,'task01':otsk0})          
    
        return render(request, "prjtask/index.html" ,{'rolelevel':rolelevel , 'prj':prj , 'tsk':tsk})

@login_required
def addproject(request):

    if request.method == "POST":
        form=AddProject(request.POST )
        
        if form.is_valid():
            name =form.cleaned_data["name"]
            pj= Projects.objects.create(name=name)
            pj.save()
            messages.info(request , "Project Saved "  )
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"prjtask/addproject.html",{'form':form})
    else:
        form = AddProject()
        return  render(request,"prjtask/addproject.html",{'form':form})        


@login_required
def action(request, id):
    user0 = User.objects.get(username=request.user.username)
    tsk0 =Task.objects.get(id=id)
    prjcomplete= Projects.objects.get(id=tsk0.project_id)
    if tsk0.status>99:
        messages.info(request , "Please note that if you want to amend 100% progress then login as Manager "  )
        return HttpResponseRedirect(reverse("index"))

    

    if request.method == "POST":
        form=Progress(request.POST )
        
        if form.is_valid():
            if (tsk0.status > 99):
                prjcomplete.completed=int(prjcomplete.completed) - 1
                prjcomplete.save(update_fields=['completed']) 
                
            else:
                pass
            status =int(form.cleaned_data["status"])
            tsk0.status = status
            tsk0.progress=request.POST["txtarea"]
            tsk0.save(update_fields=['status','progress'])
            if (tsk0.status < 99):
                tsk0.chck="Not Finished"
                tsk0.save(update_fields=['chck'])
                
                
            else:
                tsk0.chck="Completed"    
                tsk0.save(update_fields=['chck'])
                
                prjcomplete.completed=int(prjcomplete.completed) + 1
                prjcomplete.save(update_fields=['completed']) 

            messages.info(request , "Progress Updated "  )
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"prjtask/action.html",{'form':form})
    else:
        form = Progress(request.POST or None , instance=tsk0)
        tsk=tsk0.progress
        return  render(request,"prjtask/action.html",{'form':form ,'tsk0':tsk})

@login_required
def edit(request,id):
    user0 = User.objects.get(username=request.user.username)
    
    tsk0 =get_object_or_404(Task, id=id)
    prjcomplete= Projects.objects.get(id=tsk0.project_id)
    p=prjcomplete.completed
    form=Task2(request.POST or None , instance=tsk0)

    if (int(tsk0.status) > 99):
        p=prjcomplete.completed - 1
            
        
     
    if form.is_valid(): 

        tsk0.name =form.cleaned_data["name"]
        tsk0.start= form.cleaned_data["start_time"]
        tsk0.end= form.cleaned_data["expected_end"]
        tsk0.dec =form.cleaned_data["t_description"]
        tsk0.assignedto=form.cleaned_data["asignedto"]

        status =int(form.cleaned_data["status"])
        tsk0.status = status
        tsk0.save(update_fields=['status','name',
                  't_description' ,
                  'asignedto',
                  'start_time',
                  'expected_end'
        ])
        prjcomplete.completed = p
        prjcomplete.save(update_fields=['completed']) 
        if (tsk0.status > 99):
            tsk0.chck="Completed"
            
            tsk0.save(update_fields=['chck'])
            prjcomplete.completed=int(prjcomplete.completed) + 1
            prjcomplete.save(update_fields=['completed']) 
            
                
        else:
            tsk0.chck="Not Finished"    
            tsk0.save(update_fields=['chck'])
            
           

        messages.info(request , "Task Updated "  )
        return HttpResponseRedirect(reverse("index"))
    else:
        
        return render(request,"prjtask/edit.html",{'form':form })


@login_required
def search(request,id):

    # Query for requested
    try:
        task = Task.objects.filter(project_id=id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Tasks for this project not found."}, status=404)

    # Return search contents
    if request.method == "GET":
        #return JsonResponse(task.serialize())

        return JsonResponse([task.serialize() for task in task] , safe=False)


        


@login_required
def compose(request,id):
    user0 = User.objects.get(username=request.user.username)
    tsk0 =Task.objects.get(id=id)


    if request.method == "POST":
        form=Progress(request.POST )
        
        if form.is_valid():
            
            status =int(form.cleaned_data["status"])
            tsk0.status = status
            tsk0.save(update_fields=['status'])
            if (tsk0.status < 100):
                tsk0.chck="Not Finished"
                tsk0.save(update_fields=['chck'])
                
            else:
                tsk0.chck="Completed"    
                tsk0.save(update_fields=['chck'])
                #tsk0.save(update_fields=['status'])

            messages.info(request , "Progress Updated "  )
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"prjtask/action.html",{'form':form})
    else:
        form = Progress()
        return  render(request,"prjtask/action.html",{'form':form})        


@login_required
def assign(request, id):
    user0 = User.objects.get(username=request.user.username)
    prj0 =Projects.objects.get(id=id)


    if request.method == "POST":
        form=Assign(request.POST )
        
        if form.is_valid():
            name =form.cleaned_data["name"]
            start= form.cleaned_data["start_time"]
            end= form.cleaned_data["expected_end"]
            dec =form.cleaned_data["t_description"]
            assignedto=form.cleaned_data["asignedto"]
            id = id


            tsk1= Task.objects.create(name=name , start_time=start,expected_end=end,t_description=dec,asignedto  = assignedto ,project_id=id ,tuser_id=user0.id  )
            tsk1.save()
            pj1 = prj0.counttask + 1
            prj0.counttask = pj1
            prj0.save(update_fields=['counttask'])
            messages.info(request , "Task Saved "  )
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"prjtask/assign.html",{'form':form})
    else:
        form = Assign()
        return  render(request,"prjtask/assign.html",{'form':form})        


@login_required
def delete(request,id):
    user0 = User.objects.get(username=request.user.username)
    user00 = User.objects.all()
    
    tsk00 =get_object_or_404(Task, id=id)
    prjcomplete= Projects.objects.get(id=tsk00.project_id)
    p=prjcomplete.completed
    tsk0 = Task.objects.filter(project_id=tsk00.project_id).order_by('-start_time')

    if (int(tsk00.status) > 99):
        p=prjcomplete.completed - 1
        prjcomplete.completed = p
        prjcomplete.save(update_fields=['completed']) 
        
    prjcomplete.counttask = int(prjcomplete.counttask) - 1
    prjcomplete.save(update_fields=['counttask']) 
    tsk00.delete()
    messages.info(request , "Task Deleted "  )
    return  render(request,"prjtask/view.html",{'task0':tsk0,'user0':user00 , 'prj0':prjcomplete})             


@login_required
def view(request, id):
    user0 = User.objects.get(username=request.user.username)
    user00=User.objects.all()
    prj0 =Projects.objects.get(id=id)
    tsk0 = Task.objects.filter(project_id=id).order_by('-start_time')
    nw1 = datetime.now()
    nw2 = nw1.strftime("%b %d %Y, %I:%M %p")
               
    page = request.GET.get('page', 1)

    paginator = Paginator(tsk0, 10)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)        


    return  render(request,"prjtask/view.html",{'task0':tsk0,'user0':user00 , 'p':p , 'prj0':prj0 ,'nw2':nw1})        

@login_required
def deletepr(request,id):
   
    
    prjcomplete =get_object_or_404(Projects, id=id)
   
    prjcomplete.delete()
    messages.info(request , "Project Deleted "  )
    return HttpResponseRedirect(reverse("index"))
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "prjtask/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "prjtask/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    #return render(request, "prjtask/register.html" , {'form':Createlevel()})
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "prjtask/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        form=Createlevel(request.POST )
        try:
            
            if form.is_valid():
                userlevels =int(form.cleaned_data["userlevels"])

                user = User.objects.create(username=username, email=email, password=password, userlevels=userlevels )
                user.save()
                #user.userlevels
                #u#ser.save(update_fields=['userlevels'])
                

        except IntegrityError:
            return render(request, "prjtask/register.html", {
                "message": "Username already taken.","form":Createlevel()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "prjtask/register.html" , {'form':Createlevel()})