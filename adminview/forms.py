from django.forms import ModelForm
from adminview.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "picture", "category", "location"]