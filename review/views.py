from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from review.forms import ReviewForm
from review.models import ReviewEntry, Product
from django.contrib import messages
import pytz

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
            description = strip_tags(request.POST.get("description"))

            if not rating or not description:
                return JsonResponse({'status': 'FAILED', 'message': 'Rating and description are required.'}, status=400)
             # Set timezone ke Jakarta saat membuat review

            jakarta_tz = pytz.timezone('Asia/Jakarta')
            jakarta_time = timezone.now().astimezone(jakarta_tz)
            new_review = ReviewEntry(
                rating=rating,
                description=description,
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
        review.description = form.cleaned_data['description']
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
                'description': review.description,
                'date_create': jakarta_time.strftime("%d %B %Y %H:%M"), 
                'user': {
                    'username': review.user.username  # Ambil username dari user yang membuat review
                }
            }
        })
    return JsonResponse(data, safe=False)

