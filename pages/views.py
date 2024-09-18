from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,View
from .forms import ProductForm
from pages.models import Farmer,Driver,Truck,Post
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

class Farm(View):
    template_name= 'FarmerHome.html'
    def get(self, request,farmer_id, *args, **kwargs):
        products = Post.objects.filter(farmer=Farmer.objects.get(pk=farmer_id))  # Get all products from the database
        context = {

            'products': products
        }
        return render(request,self.template_name,context)
class CreateProductView(View):
    def get(self, request, farmer_id, *args, **kwargs):
        # Get the farmer by ID from the URL
        farmer = get_object_or_404(Farmer, pk=farmer_id)
        
        # Pass the farmer to the form and make the field hidden
        form = ProductForm(initial={'farmer': farmer})
        return render(request, 'createPost.html', {'form': form, 'farmer': farmer})

    def post(self, request, farmer_id, *args, **kwargs):
        # Get the farmer by ID from the URL
        farmer = get_object_or_404(Farmer, pk=farmer_id)
        
        # Bind the form with POST data and set the farmer
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = farmer  # Assign the farmer to the product
            product.save()
            return redirect('homepage')  # Redirect to homepage after saving
        return render(request, 'createPost.html', {'form': form, 'farmer': farmer})
