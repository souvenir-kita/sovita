from django.shortcuts import render, redirect   
from .forms import ProductForm
from .models import CartProduct
from django.http import HttpResponse
from django.core import serializers

def show_cart(request):
    cart_products = CartProduct.objects.all()
    
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E',
        'cart' : cart_products
    }

    return render(request, "main.html", context)

def add_product_to_cart(request, product_id):
    if request.method == 'POST':
        # Logic to add the product to the cart
        # Use product_id to find the product and add to the cart
        # Optionally get the cart_amount from the POST data
        # cart_amount = request.POST.get('cart_amount')
        # Perform your add-to-cart logic here
        return redirect('cart:create_cart.html')  # Redirect after successful addition
    else:
        # Handle case if the request method is not POST
        return redirect('cart:create_cart.html')
    # form = ProductForm(request.POST or None)

    # if form.is_valid() and request.method == "POST":
    #     form.save()
    #     return redirect('cart:show_cart')

    # context = {'form': form}
    # return render(request, "add_product_to_cart.html", context)

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