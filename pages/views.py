from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView,View
from .forms import ProductForm,OrderForm
from pages.models import Farmer,Driver,Truck,Post,Order
from datetime import datetime
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

class Farm(View):
    template_name= 'FarmerHome.html'
    def get(self, request,farmer_id, *args, **kwargs):
        farm=Farmer.objects.get(pk=farmer_id)
        products = Post.objects.filter(farmer=farm)  # Get all products from the database
        context = {
            'farmer': farm,
            'products': products,
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
            return redirect('home')  # Redirect to homepage after saving
        return render(request, 'createPost.html', {'form': form, 'farmer': farmer})
    


class DriverHomepageView(View):
    def get(self, request, driver_id, *args, **kwargs):
        # Get the current date and time
        now = datetime.now()

        # Ensure the driver exists
        driver = get_object_or_404(Driver, id=driver_id)

        # Filter orders where the associated post's delivery date is in the future
        orders = Order.objects.filter(PostId__delivery_date__gte=now, PostId__stock__gt=0, TransportId=driver)

        return render(request, 'DriverHome.html', {'orders': orders, 'driver': driver})
    

class AvailableOrdersView(View):
    def get(self, request, driver_id, *args, **kwargs):
        # Get the current date and time
        now = datetime.now()

        # Ensure the driver exists
        driver = get_object_or_404(Driver, id=driver_id)

        # Filter orders where the associated post's delivery date is in the future and not assigned to any driver
        available_posts = Post.objects.filter(delivery_date__gte=now, stock__gt=0)

        return render(request, 'available_orders.html', {'posts': available_posts, 'driver': driver})

    def post(self, request, driver_id, *args, **kwargs):
        driver = get_object_or_404(Driver, id=driver_id)
        post_id = request.POST.get('post_id')
        amount = request.POST.get('amount')

        if post_id and amount:
            post = get_object_or_404(Post, id=post_id)
            if post.stock >= int(amount):
                # Create a new order
                Order.objects.create(
                    PostId=post,
                    Amount=amount,
                    TransportId=driver
                )
                # Update the stock of the post
                post.stock -= int(amount)
                post.save()
                # Redirect to a confirmation page or the driver homepage
                return redirect('driver_homepage', driver_id=driver_id)
        return redirect('available_orders', driver_id=driver_id)
    
class FarmerPersonView(View):
    template_name= 'FarmerPerson.html'
    def get(self, request,farmer_id, *args, **kwargs):
        farmerPerson =Farmer.objects.get(pk=farmer_id)
        personName = farmerPerson.user.name
        personCountry=farmerPerson.country
        personPostalCode=farmerPerson.postal_code
        personPhone=farmerPerson.user.phone
        context = {
            'farmer': farmerPerson,
            'name': personName,
            'country':personCountry,
            'postal':personPostalCode,
            'phone':personPhone,
        }
        return render(request,self.template_name,context)
    

class PostView():
    template_name = 'show.html'

    def get(self, request, id):
      context = {}
      try:
         post_id = int(id)
         if post_id < 1:
            raise ValueError("Product id must be 1 or greater")
         post = get_object_or_404(Post, pk=post_id)
      except (ValueError, IndexError):
         # If the product id is not valid, redirect to the home page
         return HttpResponseRedirect(reverse('home'))
      

      post = get_object_or_404(Post, pk=post_id) 
      name=post.name
      stock=post.stock
      delivery=post.delivery_date
      farmer_name=post.farmer.user.name
      farmer_number=post.farmer.user.phone

      context = {
          
          'farmer_name': farmer_name,
          'farmer_number':farmer_number,
          'name': name,
          'stock': stock,
          'delivery':delivery,
        }
         
      return render(request, self.template_name, context)
