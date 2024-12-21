from django.shortcuts import render, redirect, get_object_or_404
from adminview.decorators import admin_required
from adminview.models import Product
from adminview.forms import ProductForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
import json

@admin_required
def show_admin(request):
    productEntry = Product.objects.all()
    context = {
        'productEntry' : productEntry,
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

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

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            category = request.POST.get('category')
            location = request.POST.get('location')
            image_base64 = request.POST.get('image')
            image_data = base64.b64decode(image_base64)
            image_file = ContentFile(image_data, name=f"product_{name}.jpg")
            new_product = Product.objects.create(
                name=name,
                price=int(price),
                description=description,
                category=category,
                location=location,
                picture=image_file,
            )
            new_product.save()

            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

    
@csrf_exempt
def update_flutter(request, id):
    if request.method == 'POST':  # Handle POST as update
        try:
            data = json.loads(request.body)
            product = Product.objects.get(pk=id)
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            product.category = data.get('category', product.category)
            product.location = data.get('location', product.location)
            product.save()
            return JsonResponse({'status': 'success', 'message': 'Product updated successfully!'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def show_json_random(request):
    data = Product.objects.order_by('?')[:8]
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def delete_flutter(request, id):
    if request.method == "POST":
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

