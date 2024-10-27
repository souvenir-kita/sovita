from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from adminview.models import Product
from django.contrib.auth.decorators import login_required
from django.core import serializers
from authentication.models import UserProfile

# @login_required(login_url='authentication:login')
def display_main(request):
    productEntry = Product.objects.all()
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        last_login = request.COOKIES.get('last_login')  # Get the cookie if it exists
    else:
        last_login = None  # Or you can simply omit this if not authenticated

    context = {
        'product_entry': productEntry,
        'last_login': last_login,  # Set to None if the user is not authenticated
        'name': request.user.username
    }

    return render(request, "display.html", context)

def to_landing(request):
    return render(request, 'landing_page.html')

@login_required
def profile_view(request):
    # Get the user's profile
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'profile_page.html', context)

def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user.is_authenticated:
        is_wishlisted = product.id in request.user.wishlists.values_list('product_id', flat=True)
    else:
        is_wishlisted = False
    context = {
        'product': product,
        'is_wishlisted': is_wishlisted
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
