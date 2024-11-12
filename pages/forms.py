from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Order, Farmer, Driver, Truck
from django.utils.translation import gettext_lazy as _

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
            'Amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Enter amount')}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("Correo Electrónico"))
    first_name = forms.CharField(max_length=30, label=_("Nombre"))
    last_name = forms.CharField(max_length=30, label=_("Apellido"))

    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput,
        help_text="",
    )
    password2 = forms.CharField(
        label=_("Confirmar Contraseña"),
        widget=forms.PasswordInput,
        help_text="",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'username': _("user"),
            'password1': _("Contraseña"),
            'password2': _("Confirmar Contraseña"),
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
            'country': _("País"),
            'state': _("Estado/Provincia"),
            'postal_code': _("Código Postal"),
            'phone': _("Teléfono"),
        }
        widgets = {
            'country': forms.TextInput(attrs={'placeholder': _("Ingresa tu país")}),
            'state': forms.TextInput(attrs={'placeholder': _("Ingresa tu estado o provincia")}),
            'postal_code': forms.NumberInput(attrs={'placeholder':  _("Ingresa tu código postal")}),
            'phone': forms.TextInput(attrs={'placeholder': _("Ingresa tu número de teléfono")}),
        }

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['description', 'phone']
        labels = {
            'description': _("Descripción"),
            'phone': _("Teléfono"),
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': _("Ingresa una descripción breve sobre ti")}),
            'phone': forms.TextInput(attrs={'placeholder': _("Ingresa tu número de teléfono")}),
        }

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['LicensePlate']
        labels = {
            'LicensePlate': _("Placa del Camión"),
        }
        widgets = {
            'LicensePlate': forms.TextInput(attrs={'placeholder': _("Ingresa la placa del camión")}),
        }