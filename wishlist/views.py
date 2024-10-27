import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from adminview.models import Product

@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-priority', '-added_on')
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist.html', context)

@login_required
def toggle_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        data = json.loads(request.body) if request.body else {}
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if created:
            wishlist_item.priority = data.get('priority', 2)
            wishlist_item.description = data.get('description', '')
            wishlist_item.save()
            action = 'added'
        else:
            wishlist_item.delete()
            action = 'removed'

        return JsonResponse({
            'status': 'success',
            'action': action,
            'product_id': str(product_id),
            'priority': wishlist_item.priority if action == 'added' else None,
            'description': wishlist_item.description if action == 'added' else None,
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
