from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from review.forms import ReviewForm
from review.models import ReviewEntry, Product
from django.contrib import messages
import json
import pytz
from authentication.models import UserProfile

def show_review(request, id):
    is_buyer = False
    if request.user.is_authenticated:
        is_buyer = hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'buyer'
    
    # Ambil review yang sudah ada untuk user saat ini
    user_review_ids = ReviewEntry.objects.filter(user=request.user).values_list('id', flat=True) if request.user.is_authenticated else []
    is_admin = request.user.is_staff  # Cek apakah pengguna adalah admin

    context = {
        'name': request.user.username if request.user.is_authenticated else '',
        'id': id,
        'is_buyer': is_buyer,
        'user_review_ids': user_review_ids, 
        'is_admin': is_admin,  # Tambahkan informasi tentang admin
    }
    return render(request, "review_page.html", context)

@csrf_exempt
@login_required
def create_review(request, id):
    if request.method == "POST":
        if not hasattr(request.user, 'userprofile'):
            return JsonResponse({'status': 'FORBIDDEN', 'message': 'User profile not found.'}, status=403)

        if request.user.userprofile.role != 'buyer':
            return JsonResponse({'status': 'FORBIDDEN', 'message': 'Only buyers can create reviews.'}, status=403)

        try:
            product = get_object_or_404(Product, id=id)
            rating = strip_tags(request.POST.get("rating"))
            deskripsi = strip_tags(request.POST.get("deskripsi"))

            if not rating or not deskripsi:
                return JsonResponse({'status': 'FAILED', 'message': 'Rating and deskripsi are required.'}, status=400)
            # Set timezone ke Jakarta saat membuat review
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            jakarta_time = timezone.now().astimezone(jakarta_tz)
            new_review = ReviewEntry(
                rating=rating,
                deskripsi=deskripsi,
                date_create=jakarta_time,
                user=request.user,
                product=product
            )
            new_review.save()

            return JsonResponse({'status': 'CREATED'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'FAILED', 'message': 'Invalid request method.'}, status=400)

@login_required
def edit_review(request, id):
    review = get_object_or_404(ReviewEntry, pk=id)
    product_id = review.product.id
    if request.user != review.user:
        messages.error(request, "You do not have permission to edit this review.")
        return HttpResponseRedirect(reverse('review:show_review', args=[product_id]))
    # Cek apakah user adalah pemilik review
    if review.user != request.user:
        return JsonResponse({'status': 'FORBIDDEN', 'message': 'You can only edit your own reviews.'}, status=403)

    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid() and request.method == "POST":
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        jakarta_time = timezone.now().astimezone(jakarta_tz)
        
        # Update the review instance before saving
        review.deskripsi = form.cleaned_data['deskripsi']
        review.rating = form.cleaned_data['rating']
        review.date_create = jakarta_time  # Update the date_update field
        review.save()
        form.save()
        return HttpResponseRedirect(reverse('review:show_review', args=[review.product.id]))

    context = {'form': form}
    return render(request, "edit_review.html", context)

@login_required
def delete_review(request, id):
    review = get_object_or_404(ReviewEntry, pk=id)

    # Cek apakah user adalah pemilik review
    if review.user != request.user:
        return JsonResponse({'status': 'FORBIDDEN', 'message': 'You can only delete your own reviews.'}, status=403)

    product_id = review.product.id
    review.delete()
    return HttpResponseRedirect(reverse('review:show_review', args=[product_id]))

def show_json(request, product_id):
    reviews = ReviewEntry.objects.filter(product_id=product_id).select_related('user')
    data = []
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    for review in reviews:
        jakarta_time = review.date_create.astimezone(jakarta_tz)
        data.append({
            'pk': review.id,
            'fields': {
                'rating': review.rating,
                'deskripsi': review.deskripsi,
                'date_create': jakarta_time.strftime("%d %B %Y %H:%M"), 
                'user': {
                    'username': review.user.username  # Ambil username dari user yang membuat review
                }
            }
        })
    return JsonResponse(data, safe=False)

def show_json_all(request):
    reviews = ReviewEntry.objects.all()
    data = []
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    for review in reviews:
        jakarta_time = review.date_create.astimezone(jakarta_tz)
        data.append({
            'pk': review.id,
            'fields': {
                'rating': review.rating,
                'deskripsi': review.deskripsi,
                'date_create': jakarta_time.strftime("%d %B %Y %H:%M"), 
                'user': {
                    'username': review.user.username  # Ambil username dari user yang membuat review
                }
            }
        })
    return JsonResponse(data, safe=False)

@csrf_exempt 
def get_product_reviews(request, product_id):
    if request.method == 'GET':
        try:
            reviews = ReviewEntry.objects.filter(product_id=product_id).select_related('user')
            review_list = []
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            
            for review in reviews:
                jakarta_time = review.date_create.astimezone(jakarta_tz)
                review_data = {
                    'id': str(review.id),
                    'username': review.user.username,
                    'rating': review.rating,
                    'review': review.deskripsi,  # Changed from 'deskripsi' to match Flutter
                    'date_created': jakarta_time.strftime("%d %B %Y %H:%M"),
                    'is_user_review': request.user.id == review.user.id  # Check if current user is reviewer
                }
                review_list.append(review_data)
                
            return JsonResponse({
                'status': 'success',
                'reviews': review_list
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

def check_user_role(user):
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role
    except UserProfile.DoesNotExist:
        return None

@csrf_exempt
def create_review_flutter(request, product_id):
    if request.method == 'POST':
        try:
            # Check if user is admin
            user_role = check_user_role(request.user)
            if user_role == "admin":
                return JsonResponse({
                    'status': 'error',
                    'message': 'Admins are not allowed to create reviews'
                }, status=403)

            data = json.loads(request.body)
            fields = data.get('fields', {})
            
            new_review = ReviewEntry.objects.create(
                product_id=product_id,
                user=request.user,
                rating=fields['rating'],
                deskripsi=fields['deskripsi'],
            )
            
            return JsonResponse({
                'status': 'success',
                'pk': str(new_review.pk),
                'fields': {
                    'rating': new_review.rating,
                    'deskripsi': new_review.deskripsi,
                    'date_create': new_review.date_create.strftime("%Y-%m-%d %H:%M:%S"),
                    'user': {
                        'username': new_review.user.username
                    }
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def edit_review_flutter(request, product_id):
    if request.method == "POST":
        try:
            # Check if user is admin
            user_role = check_user_role(request.user)
            if user_role == "admin":
                return JsonResponse({
                    'status': 'error',
                    'message': 'Admins are not allowed to edit reviews'
                }, status=403)

            review = ReviewEntry.objects.get(pk=product_id)
            # Check if the current user is the owner of the review
            if request.user != review.user:
                return JsonResponse(
                    {"status": "error", "message": "Not authorized"}, 
                    status=403
                )
                
            data = json.loads(request.body)
            review.rating = data["rating"]
            review.deskripsi = data["deskripsi"]
            review.save()

            return JsonResponse({"status": "success"}, status=200)
        except ReviewEntry.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Review not found"}, 
                status=404
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, 
                status=400
            )
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
def delete_review_flutter(request, product_id):
    if request.method == "POST":
        try:
            # Check if user is admin
            user_role = check_user_role(request.user)
            if user_role == "admin":
                return JsonResponse({
                    'status': 'error',
                    'message': 'Admins are not allowed to delete reviews'
                }, status=403)

            review = ReviewEntry.objects.get(pk=product_id)
            # Check if the current user is the owner of the review
            if request.user != review.user:
                return JsonResponse(
                    {"status": "error", "message": "Not authorized"}, 
                    status=403
                )
                
            review.delete()
            return JsonResponse({"status": "success"}, status=200)
        except ReviewEntry.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Review not found"}, 
                status=404
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, 
                status=400
            )
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)