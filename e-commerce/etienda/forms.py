from django import forms


class ProductForm(forms.Form):
    """Form for creating a new product"""
    title = forms.CharField(label='Product title', max_length=100)
    price = forms.DecimalField(label='Price')
    description = forms.CharField(label='Description', max_length=255, widget=forms.Textarea, required=False)
    category = forms.CharField(label='Category', max_length=100)
    image = forms.ImageField(label='Image', required=False)
