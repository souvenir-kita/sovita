from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from display.forms import ProductForm
from display.models import Product
from django.contrib.auth.decorators import login_required

@login_required(login_url='authentication:login')
def display_main(request):
    productEntry = Product.objects.all()
    context = {
        'name' : 'Bolu Bali',
        'price': 'RP20.000,00',
        'description' : 'A bolu made in Bali.',
        'location' : 'Denpasar City, Bali.',
        'shop': 'Bali Shop',
        'product_entry' : productEntry,
    }

    return render(request, "display.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("display:display_main")
    
    context = {
        'form': form
                }
    return render(request, "create_product.html", context)

def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
                'product' : product,
    }
    return render(request, 'view_product.html', context)

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('display:display_main'))
        else:
            form = ProductForm(instance=product)
    return render(request, "edit_product.html", {'form': form})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(reverse('display:display_main'))
    context = {
                'product' : product
    }
    return render(request, "delete_confirmation.html" ,context)