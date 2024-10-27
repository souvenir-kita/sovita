from django.shortcuts import render, redirect, get_object_or_404
from adminview.decorators import admin_required
from adminview.models import Product
from adminview.forms import ProductForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@admin_required
def show_admin(request):
    productEntry = Product.objects.all()
    context = {
        'productEntry' : productEntry,
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

@admin_required
def create_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('adminview:show_admin')

    context = {'form': form}
    return render(request, "create_product_admin.html", context)

@admin_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminview:show_admin'))
        else:
            form = ProductForm(instance=product)
    return render(request, "edit_product_admin.html", {'form': form})

@admin_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        return HttpResponseRedirect(reverse('adminview:show_admin'))
    context = {
                'product' : product
    }
    return render(request, "delete_product_admin.html" ,context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@admin_required
def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@admin_required
def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
@admin_required
def create_product_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    picture = request.FILES.get("picture")
    location = request.POST.get("location")
    category = request.POST.get("category")

    new_product = Product(
        name = name, price = price, description = description,
        picture = picture,  category = category, location = location,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)