from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

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
    path('Farmer/<int:farmer_id>/my-orders', views.FarmerMyOrdersView.as_view(), name='farmer_my_orders'),
    path('set_language/', views.SetLanguage.as_view(), name='set_language'),
    path('change-language/', views.LanguageChangeView.as_view(), name='change_language'),
    path('json/',views.jsonView.as_view(),name="json"),
    path('route/<int:driver_id>/<int:order_id>/', views.RouteMapView.as_view(), name='route_map'),
]   
