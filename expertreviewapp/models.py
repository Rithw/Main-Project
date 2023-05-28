from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    usertype=models.CharField(max_length=20)

class Registration(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    add=models.CharField(max_length=100)
    con=models.BigIntegerField()
    psw=models.CharField(max_length=20)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

class Company(models.Model):
    name=models.CharField(max_length=20)
    con=models.CharField(max_length=20,null=True)
    logo=models.ImageField()
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

class Vehicle(models.Model):
    name=models.CharField(max_length=20)
    cmp=models.ForeignKey(Company,on_delete=models.CASCADE)
    model=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    fuel=models.CharField(max_length=100)
    torque=models.CharField(max_length=100)
    hp=models.CharField(max_length=100)
    colors=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    groundcl=models.CharField(max_length=100)
    tiresize=models.CharField(max_length=100)
    image=models.ImageField(max_length=100)
    date=models.DateField(max_length=100)
  
    


  
class CustReview(models.Model):
    review=models.CharField(max_length=20)
    rating=models.CharField(max_length=20)
    date=models.DateField(max_length=100)
    vid=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)


class Expert(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    
    con=models.BigIntegerField()
    psw=models.CharField(max_length=20)
    exp=models.CharField(max_length=20,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

class ExpertReview(models.Model):
    review=models.CharField(max_length=20)
    rating=models.CharField(max_length=20)
    exp=models.ForeignKey(Expert,on_delete=models.CASCADE)
    date=models.DateField(max_length=100)
    vid=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    whybuy=models.CharField(max_length=100)
    whyavoid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class Question(models.Model):
    q=models.CharField(max_length=100)

class ReviewChild(models.Model):
    rid=models.ForeignKey(ExpertReview,on_delete=models.CASCADE)
    q=models.ForeignKey(Question,on_delete=models.CASCADE,null=True)
    a=models.CharField(max_length=20)
    rating=models.CharField(max_length=10,null=True)


class Request(models.Model):
    con=models.CharField(max_length=20,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    exp=models.ForeignKey(Expert,on_delete=models.CASCADE)
    status=models.CharField(max_length=20)
    
class Chat(models.Model):
    sender=models.CharField(max_length=20)
    receiver=models.CharField(max_length=20)
    date=models.CharField(max_length=20)
    message=models.CharField(max_length=400)