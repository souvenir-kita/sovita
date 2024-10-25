from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from display.models import Product

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"{product.name} was added to your wishlist.")
    else:
        wishlist_item.delete()
        messages.success(request, f"{product.name} was removed from your wishlist.")
    
    return redirect('product_detail', product_id=product_id)

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})
