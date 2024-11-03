from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView,View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import ProductForm, OrderForm, UserRegisterForm, FarmerForm, DriverForm, TruckForm
from pages.models import Farmer, Driver, Truck, Post,Order,Farmer, Driver, User
from django.views.generic import TemplateView, FormView
from datetime import datetime
from django.contrib import messages
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

class FarmerHomePageView(View):
    template_name= 'FarmerHome.html'
    def get(self, request,farmer_id, *args, **kwargs):
        farm=Farmer.objects.get(pk=farmer_id)
        products = Post.objects.filter(farmer=farm)  # Get all products from the database
        context = {
            'farmer': farm,
            'products': products,
        }
        return render(request,self.template_name,context)
    
class FarmerMyOrdersView(View):
    template_name='farmer_My_orders.html'

    def get(self, request, farmer_id, *args, **kwargs):
        # Get the current date and time
        now = datetime.now()

        # Ensure the farmer exists
        farmer = get_object_or_404(Farmer, id=farmer_id)

        # Filter orders where the associated post's delivery date is in the future
        orders = Order.objects.filter(PostId__delivery_date__gte=now, PostId__stock__gt=0, PostId__farmer=farmer )

        return render(request, self.template_name , {'orders': orders, 'farmer': farmer})
    
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
    
class RegisterSelectTypeView(TemplateView):
    template_name = 'login/register_select_type.html'

    def post(self, request, *args, **kwargs):
        user_type = request.POST.get('user_type')
        if user_type == 'farmer':
            return redirect('register_farmer')
        elif user_type == 'driver':
            return redirect('register_driver')
        else:
            messages.error(request, 'Selecciona un tipo de usuario válido.')
            return redirect('register_select_type')

class RegisterFarmerView(FormView):
    template_name = 'login/register_farmer.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'farmer_form' not in context:
            context['farmer_form'] = FarmerForm()
        return context

    def post(self, request, *args, **kwargs):
        print("POST request received en RegisterFarmerView")
        form = self.get_form()
        farmer_form = FarmerForm(request.POST)
        if form.is_valid() and farmer_form.is_valid():
            return self.form_valid(form, farmer_form)
        else:
            print("form_invalid en RegisterFarmerView")
            return self.form_invalid(form, farmer_form)

    def form_valid(self, form, farmer_form):
        print("form_valid llamado en RegisterFarmerView")
        user = form.save()
        farmer = farmer_form.save(commit=False)
        farmer.user = user
        farmer.save()
        messages.success(self.request, 'Registro de Farmer exitoso. Puedes iniciar sesión ahora.')
        return super().form_valid(form)

    def form_invalid(self, form, farmer_form):
        print("form_invalid llamado en RegisterFarmerView")
        # Imprimir errores de ambos formularios
        if not form.is_valid():
            print("Errores en UserRegisterForm:", form.errors)
        if not farmer_form.is_valid():
            print("Errores en FarmerForm:", farmer_form.errors)
        return self.render_to_response(
            self.get_context_data(form=form, farmer_form=farmer_form)
        )

class RegisterDriverView(FormView):
    template_name = 'login/register_driver.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'driver_form' not in context:
            context['driver_form'] = DriverForm()
        if 'truck_form' not in context:
            context['truck_form'] = TruckForm()
        return context

    def post(self, request, *args, **kwargs):
        print("POST request received en RegisterDriverView")
        form = self.get_form()
        driver_form = DriverForm(request.POST)
        truck_form = TruckForm(request.POST)

        if form.is_valid() and driver_form.is_valid() and truck_form.is_valid():
            return self.form_valid(form, driver_form, truck_form)
        else:
            print("form_invalid en RegisterDriverView")
            return self.form_invalid(form, driver_form, truck_form)

    def form_valid(self, form, driver_form, truck_form):
        print("form_valid llamado en RegisterDriverView")
        user = form.save()
        
        # Guardar el Driver
        driver = driver_form.save(commit=False)
        driver.user = user
        driver.save()
        
        # Guardar el Truck
        truck = truck_form.save(commit=False)
        truck.DriverId = driver
        truck.save()
        
        messages.success(self.request, 'Registro de Driver y Truck exitoso. Puedes iniciar sesión ahora.')
        return super().form_valid(form)

    def form_invalid(self, form, driver_form, truck_form):
        print("form_invalid llamado en RegisterDriverView")
        # Imprimir errores de los formularios
        if not form.is_valid():
            print("Errores en UserRegisterForm:", form.errors)
        if not driver_form.is_valid():
            print("Errores en DriverForm:", driver_form.errors)
        if not truck_form.is_valid():
            print("Errores en TruckForm:", truck_form.errors)
        
        #mensajes de error para el usuario
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f"{field}: {error}")
        if not driver_form.is_valid():
            for field, errors in driver_form.errors.items():
                for error in errors:
                    messages.error(self.request, f"{field}: {error}")
        if not truck_form.is_valid():
            for field, errors in truck_form.errors.items():
                for error in errors:
                    messages.error(self.request, f"{field}: {error}")

        return self.render_to_response(
            self.get_context_data(form=form, driver_form=driver_form, truck_form=truck_form)
        )

class UserLoginView(LoginView):
    template_name = 'login/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Intentamos redirigir al Farmer si existe
        try:
            farmer = user.farmer
            return redirect('Farmer', farmer_id=farmer.id)
        except Farmer.DoesNotExist:
            pass

        # Intentamos redirigir al Driver si existe
        try:
            driver = user.driver
            return redirect('driver_homepage', driver_id=driver.id)
        except Driver.DoesNotExist:
            pass

        # Si no es ni Farmer ni Driver, redirigimos al home
        messages.error(self.request, 'No tienes un perfil de Farmer o Driver asociado.')
        return redirect('home')
    
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Cierra la sesión del usuario
        logout(request)        
        # Redirige al usuario a la página de inicio o cualquier otra página
        return redirect('home')

class FarmerPersonView(View):
    template_name= 'FarmerPerson.html'
    def get(self, request,id, *args, **kwargs):
        farmerPerson =Farmer.objects.get(pk=id)
        personCountry=farmerPerson.country
        personPostalCode=farmerPerson.postal_code

        user_id= farmerPerson.user_id
        user= get_object_or_404(User,pk=user_id)
        name=user.name
        phone=user.phone
        context = {
            'name':name,
            'farmer': farmerPerson,
            'country':personCountry,
            'postal':personPostalCode,
            'phone':phone,
        }
        return render(request,self.template_name,context)
    
class PostView(View):
    template_name = 'show.html'

    def get(self, request, id):
      post = get_object_or_404(Post, pk=id) 
      name=post.name
      stock=post.stock
      country= post.farmer.country
      origin=post.Origin
      destination= post.Destination
      delivery=post.delivery_date
      farmer_id=post.farmer_id
      userId=post.farmer.user_id
      user= get_object_or_404(User,pk=userId)
      farmerName=user.name
      farmerPhone=user.phone      

      context = {      
          'farmer_id':farmer_id,    
          'farmer_name': farmerName,
          'name': name,
          'stock': stock,
          'delivery':delivery,
          'country':country,
          'origin':origin,
          'destination':destination,
          'phone':farmerPhone
        }         
      return render(request, self.template_name, context)

class ErrorView(TemplateView):
    template_name='error_page.html'


class LandingPageView(TemplateView):
    template_name='landingPage.html'
