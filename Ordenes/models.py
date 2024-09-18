from django.db import models

class User(models.Model):
    Name= models.CharField(max_length=20)
    Phone_Number= models.CharField(max_length=20)
    Email_Address=models.CharField(max_length=50)
class Farmer(models.Model):
    FarmerId=models.AutoField(max_length=None,primary_key=True)
    Country=models.CharField(max_length=50)
    State=models.CharField(max_length=50)    
    Postal_Code=models.CharField(max_length=10)
class Driver(models.Model):
    DriverId=models.AutoField(max_length=None,primary_key=True)
    Description=models.CharField(max_length=200)
class Truck(models.Model):
    TruckId=models.AutoField(max_length=None,primary_key=True)
    DriverId=models.ForeignKey('Driver',on_delete=models.CASCADE,null=False)
    LicensePlate=models.CharField(max_length=6)
class Post(models.Model):
    PostId=models.AutoField(max_length=None,primary_key=True)
    FarmerId=models.ForeignKey('Farmer',on_delete=models.CASCADE,null=False)
    Name= models.CharField(max_length=20)
    Stock=models.IntegerField()
    DeliveryDate= models.DateField()
    Description= models.CharField(max_length=200)
    Fare=models.IntegerField()
    ArrivalDate=models.DateField()
    LocationOrigin=models.CharField(max_length=50)
    LocationArrival=models.CharField(max_length=50)
class Order(models.Model):
    PostId=models.ForeignKey('Post',on_delete=models.CASCADE,null=False)
    TransportId=models.ForeignKey('Driver',on_delete=models.CASCADE,null=False)
    Amount= models.IntegerField()

