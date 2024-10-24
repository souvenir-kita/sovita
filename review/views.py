from django.shortcuts import render, get_object_or_404  # Tambahkan import redirect di baris ini
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.html import strip_tags
from review.forms import ReviewForm
from review.models import ReviewEntry
from display.models import Product

def show_review(request, id):
    context = {
        'name': request.user.username,
        'id': id
    }
    return render(request, "review_page.html", context)

@csrf_exempt
@require_POST
def create_review(request, id):
    product = Product.objects.get(pk=id)
    rating = strip_tags(request.POST.get("rating"))
    description = strip_tags(request.POST.get("description"))
    date_create = timezone.now()
    user = request.user
    new_review = ReviewEntry(
        rating=rating, description=description,
        date_create=date_create,
        user=user, product=product
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)

def edit_review(request, id):
    review = ReviewEntry.objects.get(pk = id)
    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('review:show_review'))
    context = {'form': form}
    return render(request, "edit_review.html", context)

def delete_review(request, id):
    review = ReviewEntry.objects.get(pk = id)
    review.delete()
    return HttpResponseRedirect(reverse('review:show_review'))

def show_json(request):
    data = ReviewEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")