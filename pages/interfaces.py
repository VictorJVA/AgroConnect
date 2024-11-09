from abc import ABC, abstractmethod
from django.http import HttpRequest

class FarmerDataAccessInterface(ABC):
    @abstractmethod
    def get_farmer(self, farmer_id):
        pass

    @abstractmethod
    def get_products(self, farmer):
        pass

class OrderDataAccessInterface(ABC):
    @abstractmethod
    def get_orders(self, farmer):
        pass

    @abstractmethod
    def get_available_orders(self):
        pass

class DriverDataAccessInterface(ABC):
    @abstractmethod
    def get_driver(self, driver_id):
        pass