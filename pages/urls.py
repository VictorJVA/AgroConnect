from django.urls import path
from .views import HomePageView,Farm,CreateProductView,DriverHomepageView,AvailableOrdersView, FarmerPersonView, PostView, ErrorView

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("Farmer/<int:farmer_id>/",Farm.as_view(),name="Farmer"),
    path('create/<int:farmer_id>/', CreateProductView.as_view(), name='create_product'),
    path('driver/<int:driver_id>/', DriverHomepageView.as_view(), name='driver_homepage'),
    path('driver/<int:driver_id>/available-orders/', AvailableOrdersView.as_view(), name='available_orders'),
    path("driver/<int:driver_id>/<int:farmer_id>", FarmerPersonView.as_view(), name="farmer_profile"),
    path("post/<int:post_id>/", PostView.as_view(), name="show_post"),
    path("error/", ErrorView.as_view(),name='error')
]