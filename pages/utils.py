from pages.models import Farmer, Driver, Post, Order
from .interfaces import FarmerDataAccessInterface, OrderDataAccessInterface, DriverDataAccessInterface
from django.shortcuts import get_object_or_404
from datetime import datetime

class FarmerDataAccess(FarmerDataAccessInterface):
    def get_farmer(self, farmer_id):
        return get_object_or_404(Farmer, pk=farmer_id)

    def get_products(self, farmer):
        return Post.objects.filter(farmer=farmer)


class OrderDataAccess(OrderDataAccessInterface):
    def get_orders(self, farmer):
        now = datetime.now()
        return Order.objects.filter(PostId__delivery_date__gte=now, PostId__stock__gt=0, PostId__farmer=farmer)

    def get_available_orders(self):
        now = datetime.now()
        return Post.objects.filter(delivery_date__gte=now, stock__gt=0)


class DriverDataAccess(DriverDataAccessInterface):
    def get_driver(self, driver_id):
        return get_object_or_404(Driver, pk=driver_id)