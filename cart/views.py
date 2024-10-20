from django.shortcuts import render, redirect   
from .forms import ProductForm
from .models import CartProduct

def show_cart(request):
    cart_products = CartProduct.objects.all()
    
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E',
        'cart' : cart_products
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('cart:show_cart')

    context = {'form': form}
    return render(request, "add_product_to_cart.html", context)