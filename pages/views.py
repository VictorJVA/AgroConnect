from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView,View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import ProductForm, OrderForm, UserRegisterForm, FarmerForm, DriverForm, TruckForm
from pages.models import Farmer, Driver, Truck, Post,Order,Farmer, Driver, User, Order
from django.views.generic import TemplateView, FormView
from datetime import datetime
from django.contrib import messages
from .interfaces import FarmerDataAccessInterface, OrderDataAccessInterface, DriverDataAccessInterface
from .utils import FarmerDataAccess, OrderDataAccess, DriverDataAccess
from django.utils.translation import activate
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your views here.
class jsonView(View):
    def get(self, request, *args, **kwargs):
        now = timezone.now()

        orders = Order.objects.filter(PostId__arrival_date__gt=now)
        posts_data = []
        for order in orders:
            post = order.PostId 
            posts_data.append({
                'post_id': post.id,
                'farmer_id': post.farmer.id,
                'name': post.name,
                'stock': post.stock,
                'delivery_date': post.delivery_date,
                'description': post.description,
                'fare': post.fare,
                'arrival_date': post.arrival_date,
                'origin': post.Origin,
                'destination': post.Destination,
            })
        return JsonResponse(posts_data, safe=False)

class RouteMapView(View):
    def get(self, request, driver_id, order_id, *args, **kwargs):
        post = get_object_or_404(Post, id=order_id)

        context = {
            'google_maps_api_key': 'AIzaSyAcpt3YUZb-WCQ9JqBMyjy6lMEDJot29lM',
            'destination': post.Destination,
            'driver_id': driver_id,  # Include driver_id in the context if needed
        }

        return render(request, 'route_map.html', context)

class HomePageView(TemplateView):
    template_name = 'home.html'

class FarmerHomePageView(View):
    template_name = 'FarmerHome.html'

    def __init__(self, farmer_data_access: FarmerDataAccessInterface = FarmerDataAccess()):
        self.farmer_data_access = farmer_data_access

    def get(self, request, farmer_id, *args, **kwargs):
        farm = self.farmer_data_access.get_farmer(farmer_id)
        products = self.farmer_data_access.get_products(farm)
        context = {
            'farmer': farm,
            'products': products,
        }
        return render(request, self.template_name, context)
    
class FarmerMyOrdersView(View):
    template_name = 'farmer_My_orders.html'

    def __init__(self, order_data_access: OrderDataAccessInterface = OrderDataAccess()):
        self.order_data_access = order_data_access

    def get(self, request, farmer_id, *args, **kwargs):
        farmer = get_object_or_404(Farmer, id=farmer_id)
        orders = self.order_data_access.get_orders(farmer)
        return render(request, self.template_name, {'orders': orders, 'farmer': farmer})
    
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
            
            # Redirect to the FarmerHomePageView with the farmer_id
            return redirect(reverse('Farmer', args=[farmer.id]))
        
        return render(request, 'createPost.html', {'form': form, 'farmer': farmer})


class DriverHomepageView(View):
    def __init__(self, driver_data_access: DriverDataAccessInterface = DriverDataAccess()):
        self.driver_data_access = driver_data_access

    def get(self, request, driver_id, *args, **kwargs):
        driver = self.driver_data_access.get_driver(driver_id)
        now = datetime.now()
        orders = Order.objects.filter(PostId__delivery_date__gte=now, PostId__stock__gt=0, TransportId=driver)
        return render(request, 'DriverHome.html', {'orders': orders, 'driver': driver})
    

class AvailableOrdersView(View):
    def __init__(self, driver_data_access: DriverDataAccessInterface = DriverDataAccess(), order_data_access: OrderDataAccessInterface = OrderDataAccess()):
        self.driver_data_access = driver_data_access
        self.order_data_access = order_data_access

    def get(self, request, driver_id, *args, **kwargs):
        driver = self.driver_data_access.get_driver(driver_id)
        available_posts = self.order_data_access.get_available_orders()
        return render(request, 'available_orders.html', {'posts': available_posts, 'driver': driver})

    def post(self, request, driver_id, *args, **kwargs):
        driver = self.driver_data_access.get_driver(driver_id)
        post_id = request.POST.get('post_id')
        amount = request.POST.get('amount')

        if post_id and amount:
            post = get_object_or_404(Post, id=post_id)
            if post.stock >= int(amount):
                Order.objects.create(
                    PostId=post,
                    Amount=amount,
                    TransportId=driver
                )
                post.stock -= int(amount)
                post.save()
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

        #user_id= farmerPerson.user_id
        #user= get_object_or_404(User,pk=user_id)
        name=farmerPerson.user
        phone= farmerPerson.phone
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
      farmer_id=post.farmer.id
      #userId=post.farmer.user
      #user= get_object_or_404(User,pk=userId)
      farmerName= post.farmer.user
      farmerPhone= post.farmer.phone      

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


class SetLanguage(TemplateView):
    template_name='setLanguage.html'

    def post(self, request, *args, **kwargs):
        # Obtiene el idioma seleccionado desde los datos POST (por ejemplo: 'es' o 'en')
        lang_code = request.POST.get('language')

        # Verifica que el código de idioma esté en los idiomas permitidos en settings
        if lang_code in dict(settings.LANGUAGES):
            # Cambia el idioma de la sesión y activa el idioma seleccionado
            request.session['django_language'] = lang_code
            activate(lang_code)

        # Redirige a la página de inicio o a otra URL según sea necesario
        return redirect('home')

    #def get(self, request, *args, **kwargs):
        # Obtiene el idioma seleccionado desde los parámetros GET (ejemplo: ?lang=en)
        #lang_code = request.GET.get('language')

        #if lang_code:
            #activate(lang_code)
        #return self.render_to_response(self.get_context_data())

class LanguageChangeView(View):
    def post(self, request, *args, **kwargs):
        # Obtén el idioma del formulario enviado
        language = request.POST.get('language')
        # Cambia el idioma usando 'activate'
        if language:
            activate(language)
            request.session['LANGUAGE_SESSION_KEY'] = language  # Guarda el idioma en la sesión
        return HttpResponseRedirect(reverse('change_language'))
    
    def get(self, request, *args, **kwargs):
        # Renderiza la plantilla para seleccionar idioma
        return render(request, 'change_language.html')