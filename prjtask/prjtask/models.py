from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.db import models
from datetime import datetime, timedelta
import datetime


class User(AbstractUser):
    ulevel=(
        (2, "worker"),
        (1, "manager")
    )
    userlevels=models.IntegerField(choices=ulevel , default = 2, blank = True)
    def __str__(self):

        return f'{self.username}{self.userlevels}'
    
    
class Projects(models.Model):
    name = models.CharField(max_length=150)
    
    start = models.DateTimeField(auto_now=True )
    end      = models.DateTimeField(null=True) 
    status = models.IntegerField(default=0)
    counttask = models.IntegerField(default=0)
    #task =models.ManyToManyField(Task, blank=True, related_name="task")
    completed = models.IntegerField(default=0)
    not_completed =models.IntegerField(default=0)
    status2 = models.BooleanField(default=False)
    complete = models.IntegerField(default=0)
    
    class Meta:
       
        ordering = ['name']
        
    
    def __str__(self):
        return  self.name

class Task(models.Model) :
    name  = models.CharField(max_length=200)
    t_description = models.TextField(max_length=1000)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    tuser=models.ForeignKey(User, on_delete=models.CASCADE, related_name="tusertask")
    start_time    = models.DateTimeField(auto_now_add=False )
    end_time      = models.DateTimeField(null=True) 
    status = models.IntegerField(default=0)   
    asignedto  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asignedtotask")
    expected_end    = models.DateTimeField(null=True )
    progress = models.TextField(max_length=2000 , null=True)
    chck=models.CharField(max_length=100)
    status2=models.BooleanField(default=False)
     

    def __str__(self):
        return  self.name

    def serialize(self):
        return {   
            "name":self.name,
            "t_description":self.t_description ,
            "tuser":self.tuser.username,
            "start_time": self.start_time.strftime("%b %d %Y, %I:%M %p"),
            "expected_end": self.expected_end.strftime("%b %d %Y, %I:%M %p"),
            "status": self.status,
            "status2": self.status2,
            "project": self.project.name,
            "id":self.id,
            "chck":self.chck,
            "progress":self.progress
             
        } 

class Comments(models.Model):
    date = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=True)
    title = models.CharField(max_length=120 ,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="taskcomments")

    def __str__(self):
        return self.title    
        