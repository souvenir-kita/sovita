from django.forms import ModelForm
from display.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "picture", "location", "shop"]