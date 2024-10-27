from django.shortcuts import render, redirect   
from .forms import ProductForm
from .models import CartProduct, Cart
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from adminview.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.db.models import Q

@login_required
def show_cart(request):
    cart_products = CartProduct.objects.filter(cart__user=request.user)
    
    context = {
        'cart': cart_products,
    }

    return render(request, "show_cart.html", context)

def add_product_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)

    amount = int(request.POST.get('cart_amount', 1))

    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'amount': amount}
    )

    if not created:
        cart_product.amount += amount
        cart_product.save()

    return redirect('display:display_main')

@login_required
def edit_cart_product(request, id):
    cart_product = get_object_or_404(CartProduct, id=id, cart__user=request.user)

    if request.method == "POST":
        new_amount = request.POST.get("amount")
        if new_amount and new_amount.isdigit():
            cart_product.amount = int(new_amount)
            cart_product.save()
            return redirect('cart:show_cart')

        return HttpResponse("Invalid amount", status=400)

    return render(request, "edit_cart_product.html", {'cart_product': cart_product})

@login_required
def delete_cart_product(request, id):
    cart_product = get_object_or_404(CartProduct, id=id, cart__user=request.user)

    if request.method == "POST":
        cart_product.delete()
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        # For regular form submission, redirect
        return redirect('cart:show_cart')

    return render(request, "confirm_delete_cart_product.html", {'cart_product': cart_product})



@require_POST
def update_note(request, id):
    try:
        cart_product = CartProduct.objects.get(id=id, cart__user=request.user)
        data = json.loads(request.body)
        note = data.get('note', '').strip()
        
        if len(note) > 144:
            return JsonResponse({
                'success': False,
                'error': 'Note is too long (maximum 144 characters)'
            }, status=400)
            
        cart_product.note = note
        cart_product.save()
        
        return JsonResponse({
            'success': True,
            'note': note
        })
    except CartProduct.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Cart item not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def inc_amount(request, id):
    cart_item = get_object_or_404(CartProduct, id=id)
    cart_item.amount += 1
    cart_item.save()
    return JsonResponse({'success': True, 'new_amount': cart_item.amount, 'new_total_price': cart_item.amount * cart_item.product.price})

def dec_amount(request, id):
    cart_item = get_object_or_404(CartProduct, id=id)
    if cart_item.amount > 1:
        cart_item.amount -= 1
        cart_item.save()
    return JsonResponse({'success': True, 'new_amount': cart_item.amount, 'new_total_price': cart_item.amount * cart_item.product.price})

def show_xml(request):
    data = CartProduct.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = CartProduct.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = CartProduct.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = CartProduct.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")