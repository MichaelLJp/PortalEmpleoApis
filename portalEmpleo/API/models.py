from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class kindId(models.Model):
    name = models.CharField(max_length=30, blank=True)
    def __str__(self): return self.name

class State(models.Model):
    name = models.CharField(max_length=30, blank=True)
    def __str__(self): return self.name 

class Candidate(models.Model):
    user = models.ForeignKey(User,related_name='candidato',on_delete=models.CASCADE)
    othersName = models.CharField(max_length=200,null=True,blank=True)
    othersLastName = models.CharField(max_length=200,null=True,blank=True)
    kindId = models.ForeignKey(kindId, on_delete=models.CASCADE)       
    numberId =  models.CharField(max_length=30)
    profession = models.CharField(max_length=500)
    description = models.CharField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Offers(models.Model):
    title = models.CharField(max_length=100, null=True)
    salary = models.IntegerField(null = True, default = 0)
    description = models.CharField(max_length=400)
    state = models.ForeignKey(State,related_name='state',null=True,on_delete=models.SET_NULL,default='Activo')
    creatorUser = models.ForeignKey(User,related_name='creatorUser',null=True,on_delete=models.SET_NULL)
    updaterUser = models.ForeignKey(User,related_name='updaterUser',null=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self): return self.title 

class Postulation(models.Model):
    offers = models.ForeignKey(Offers, related_name='offers', on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, related_name='candidate', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)







