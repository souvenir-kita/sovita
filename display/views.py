from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from adminview.models import Product
from django.contrib.auth.decorators import login_required
from django.core import serializers

@login_required(login_url='authentication:login')
def display_main(request):
    productEntry = Product.objects.all()
    context = {
        'product_entry' : productEntry,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "display.html", context)

def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
                'product' : product,
                'is_wishlisted' : product.id in request.user.wishlists.values_list('product_id', flat=True)
    }
    return render(request, 'view_product.html', context)

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
