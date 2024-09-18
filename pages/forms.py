from django import forms
from .models import Post, Order

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