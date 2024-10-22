from django.shortcuts import render, redirect   
from .forms import ProductForm
from .models import CartProduct, Cart
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from display.models import Product


def show_cart(request):
    cart_products = CartProduct.objects.all()
    
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E',
        'cart' : cart_products,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def add_product_to_cart(request, id):
    # Get the product by ID
    product = get_object_or_404(Product, id=id)
    
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the amount from the form data
    amount = int(request.POST.get('cart_amount', 1))

    # Get or create the CartProduct entry
    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'amount': amount}
    )

    # If the CartProduct already exists, update the amount
    if not created:
        cart_product.amount += amount
        cart_product.save()

    # Redirect or return a response
    return redirect('display:display_main')

def show_xml(request):
    data = CartProduct.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = CartProduct.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = CartProduct.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = CartProduct.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")