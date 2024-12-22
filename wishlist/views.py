import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from adminview.models import Product
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def remove_wishlist_flutter(request, product_id):
    user = request.user
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    try:
        if request.method == 'POST':
            # user = request.user
            product = Product.objects.get(pk=product_id)
            
            wishlist_item = Wishlist.objects.get(user=user, product=product)
            wishlist_item.delete()
            return JsonResponse({"status": "success"}, status=200)
    except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

    # try:
    #     product = Product.objects.get(id=product_id)
    # except Product.DoesNotExist:
    #     return Response({'error': 'Product not found'}, status=404)

    # wishlist_item = Wishlist.objects.filter(user=user, product=product).first()

    # if wishlist_item:
    #     wishlist_item.delete()
    #     return Response({'message': 'Product removed from wishlist'}, status=200)
    # else:
    #     Wishlist.objects.create(user=user, product=product)
    #     return Response({'message': 'Product added to wishlist'}, status=201)

@csrf_exempt
def add_wishlist_flutter(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        product =get_object_or_404(Product, product_id)
        wishlist = Wishlist.objects.create(
            user = request.user,
            product = product.pk,
            description = data["description"],
            priority = int(data["priority"]),
        )
        wishlist.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def update_wishlist_flutter(request):
    if request.method == 'POST':  # Handle POST as update
        try:
            data = json.loads(request.body)
            wishlist = Wishlist.objects.get(data["productId"])
            wishlist.description = data["description"],
            wishlist.priority = data["priority"],
            wishlist.save()
            return JsonResponse({'status': 'success', 'message': 'Wishlist updated successfully!'})
        except Wishlist.DoesNotExist:
            return JsonResponse({'error': 'Wishlist not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def show_json(request):
    data = Wishlist.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

