from django.urls import path
from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("Farmer",HomePageView.as_view(),name="Farmer")
]