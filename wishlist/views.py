from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from display.models import Product

@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        # Product was added to the wishlist
        action = 'added'
    else:
        # Product was already in the wishlist, so it was removed
        wishlist_item.delete()
        action = 'removed'
    
    return JsonResponse({'status': 'success', 'action': action, 'product_id': str(product_id)})
