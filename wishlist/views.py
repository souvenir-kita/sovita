from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from display.models import Product

@login_required
def show_wishlist(request):
    wishlist_items = Product.objects.filter(wishlist_items__user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        action = 'added'
    else:
        wishlist_item.delete()
        action = 'removed'
    
    return JsonResponse({'status': 'success', 'action': action, 'product_id': str(product_id)})
