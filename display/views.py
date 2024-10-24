from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from display.forms import ProductForm
from display.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import serializers

@login_required(login_url='authentication:login')
def display_main(request):
    productEntry = Product.objects.all()
    context = {
        'product_entry' : productEntry,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "display.html", context)

def create_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("display:display_main")
    
    context = {
        'form': form
                }
    return render(request, "create_product.html", context)

@csrf_exempt
@require_POST
def create_product_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    picture = request.FILES.get("picture")
    location = request.POST.get("location")
    shop = request.POST.get("shop")

    new_product = Product(
        name = name, price = price, description = description,
        picture = picture, location = location, shop = shop,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
                'product' : product,
    }
    return render(request, 'view_product.html', context)

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


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(reverse('display:display_main'))
    context = {
                'product' : product
    }
    return render(request, "delete_confirmation.html" ,context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def search(request):
    searched = request.GET.get('searched', '')
    if searched:
        products = Product.objects.filter(name__icontains=searched)
    else:
        products = []
    return render(request, "search.html", {'searched': searched, 'products': products})
