from django import forms
from .models import Post

class ProductForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'stock', 'delivery_date', 'description', 'fare', 'arrival_date', 'Origin', 'Destination']
        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }