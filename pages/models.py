from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Farmer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    country = models.TextField(max_length=50)
    state = models.TextField(max_length=50)
    postal_code = models.IntegerField()

class Post(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    stock = models.IntegerField()
    delivery_date = models.DateTimeField()
    description = models.TextField()
    fare = models.IntegerField()
    arrival_date = models.DateTimeField()
    Origin = models.TextField(max_length=50)
    Destination = models.TextField(max_length=50)