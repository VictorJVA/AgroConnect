from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path('register/', views.RegisterSelectTypeView.as_view(), name='register_select_type'),
    path('register/farmer/', views.RegisterFarmerView.as_view(), name='register_farmer'),
    path('register/driver/', views.RegisterDriverView.as_view(), name='register_driver'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("Farmer/<int:farmer_id>/",views.FarmerHomePageView.as_view(),name="Farmer"),
    path('create/<int:farmer_id>/', views.CreateProductView.as_view(), name='create_product'),
    path('driver/<int:driver_id>/', views.DriverHomepageView.as_view(), name='driver_homepage'),
    path('driver/<int:driver_id>/available-orders/', views.AvailableOrdersView.as_view(), name='available_orders'),
    path("post/<int:id>/", views.PostView.as_view(), name="show_post"),
    path("error/", views.ErrorView.as_view(),name='error'),
    path('person/<int:id>', views.FarmerPersonView.as_view(), name='farmer_person'),
    path('Farmer/<int:farmer_id>/my-orders', views.FarmerMyOrdersView.as_view(), name='farmer_my_orders')
]    