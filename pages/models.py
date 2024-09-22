from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class Post(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    delivery_date = models.DateTimeField()
    description = models.CharField(max_length=100)
    fare = models.IntegerField()
    arrival_date = models.DateTimeField()
    Origin = models.CharField(max_length=50)
    Destination = models.CharField(max_length=50)

class Truck(models.Model):
    TruckId = models.AutoField(primary_key=True)
    DriverId = models.ForeignKey('Driver', on_delete=models.CASCADE)
    LicensePlate = models.CharField(max_length=6)

class Order(models.Model):
    PostId=models.ForeignKey('Post',on_delete=models.CASCADE,null=False)
    TransportId=models.ForeignKey('Driver',on_delete=models.CASCADE,null=False)
    Amount= models.IntegerField()
