from django.shortcuts import render, redirect   
from .forms import ProductForm
from .models import CartProduct, Cart
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from adminview.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CartProductSerializer
from django.views.decorators.csrf import csrf_exempt

@login_required
def show_cart(request):
    sort = request.GET.get('sort', 'alphabet_asc')
    
    # Get the cart for the current user
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart:
        # If no cart exists for the user, return an empty context
        cart_products = CartProduct.objects.none()
    else:
        # Get the cart products related to this cart
        cart_products = CartProduct.objects.filter(cart=cart)
        
        # Apply sorting based on the product's name explicitly
        if sort == 'alphabet_asc':
            cart_products = sorted(cart_products, key=lambda cp: cp.product.name.lower())
        elif sort == 'alphabet_dsc':
            cart_products = sorted(cart_products, key=lambda cp: cp.product.name.lower(), reverse=True)
    
    context = {
        'cart': cart,
        'cart_products': cart_products,
        'current_sort': sort,
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
@csrf_exempt
def add_product_to_cart_with_note(request, id):
    # Ensure the request is a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    # Get the product object
    product = get_object_or_404(Product, id=id)

    # Retrieve or create a cart for the current user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get the amount and note from the POST request
    amount = int(request.POST.get('cart_amount', 1))  # Default to 1 if not provided
    note = request.POST.get('cart_note', None)  # Optional note field

    # Retrieve or create a CartProduct object
    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'amount': amount, 'note': note}  # Add note to defaults
    )

    # If the CartProduct already exists, update the amount and optionally the note
    if not created:
        cart_product.amount += amount
        if note:  # Update the note if a new one is provided
            cart_product.note = note
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

def show_all_cart(request):
    data = Cart.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@require_POST
def sort_cart(request):
    try:
        data = json.loads(request.body)
        sort_option = data.get('sort')
        
        # Get cart items for the current user
        cart = Cart.objects.filter(user=request.user)
        
        # Apply sorting
        if sort_option == 'alphabet_asc':
            cart = cart.order_by('product__name')
        elif sort_option == 'alphabet_dsc':
            cart = cart.order_by('-product__name')
            
        # Render the cart items template
        html = render_to_string('cart/_cart_items.html', {
            'cart': cart,
            'csrf_token': request.CSRF_token(),  # Pass CSRF token to template
        }, request=request)
        
        # Return the HTML directly
        return HttpResponse(html)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def show_cart_json(request):
    # Fetch the cart associated with the currently authenticated user
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        # Build the JSON response without including the cart ID
        response_data = {
            "pk": str(cart.id),
            "user": request.user.id,
            "created_at": cart.created_at,
        }
        return JsonResponse(response_data, safe=False)
    else:
        # If the cart does not exist for the user
        return JsonResponse({"error": "No cart found for the current user"}, status=404)
    
def user_json(request, id):
    data = CartProduct.objects.filter(cart__id=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def user_cart_products(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart:
        # If no cart exists for the user, return an empty context
        cart_products = CartProduct.objects.none()
    else:
        # Get the cart products related to this cart
        cart_products = CartProduct.objects.filter(cart=cart)
    
    return HttpResponse(serializers.serialize("json", cart_products), content_type="application/json")



    