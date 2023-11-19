from django import forms
from django.core.validators import MinValueValidator

# App imports
from etienda import validators


class ProductForm(forms.Form):
    """Form for creating a new product"""
    title = forms.CharField(label='Product title', max_length=100,
                            validators=[validators.validate_capitalized])
    price = forms.DecimalField(label='Price', validators=[MinValueValidator(0.0)])
    description = forms.CharField(label='Description', max_length=255, widget=forms.Textarea,
                                  required=False)
    category = forms.CharField(label='Category', max_length=100)
    image = forms.ImageField(label='Image', required=False)
