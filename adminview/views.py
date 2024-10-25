from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def show_admin(request):
    productEntry = Product.objects.all()
    context = {
        'product_entry' : productEntry,
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('display:display_main'))
        else:
            form = ProductForm(instance=product)
    return render(request, "edit_product.html", {'form': form})