from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Order, Farmer, Driver, Truck

class ProductForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'stock', 'delivery_date', 'description', 'fare', 'arrival_date', 'Origin', 'Destination']
        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Amount']
        widgets = {
            'Amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo Electrónico')
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="",
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput,
        help_text="",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'username': 'Nombre de Usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['country', 'state', 'postal_code', 'phone']
        labels = {
            'country': 'País',
            'state': 'Estado/Provincia',
            'postal_code': 'Código Postal',
            'phone': 'Teléfono',
        }
        widgets = {
            'country': forms.TextInput(attrs={'placeholder': 'Ingresa tu país'}),
            'state': forms.TextInput(attrs={'placeholder': 'Ingresa tu estado o provincia'}),
            'postal_code': forms.NumberInput(attrs={'placeholder': 'Ingresa tu código postal'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingresa tu número de teléfono'}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['description', 'phone']
        labels = {
            'description': 'Descripción',
            'phone': 'Teléfono',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Ingresa una descripción breve sobre ti'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingresa tu número de teléfono'}),
        }

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['LicensePlate']
        labels = {
            'LicensePlate': 'Placa del Camión',
        }
        widgets = {
            'LicensePlate': forms.TextInput(attrs={'placeholder': 'Ingresa la placa del camión'}),
        }