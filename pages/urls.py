from django.urls import path
from .views import HomePageView,Farm,CreateProductView

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("Farmer/<int:farmer_id>/",Farm.as_view(),name="Farmer"),
    path('create/<int:farmer_id>/', CreateProductView.as_view(), name='create_product'),
]