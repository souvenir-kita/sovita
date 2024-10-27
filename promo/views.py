from django.shortcuts import render
from django.utils.html import strip_tags
from promo.models import Promo
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from adminview.decorators import admin_required

# Yang perlu diimplement:
# 1. Validasi tanggal, only present/past
# 2. Kasih pesan kalau kode sudah ada

@admin_required
def show_promo(request):
    return render(request, "main_promo.html")

@csrf_exempt
@require_POST
@admin_required
def add_promo(request):
    nama = strip_tags(request.POST.get("nama"))
    kode = strip_tags(request.POST.get("kode"))
    potongan = strip_tags(request.POST.get("potongan"))
    deskripsi = strip_tags(request.POST.get("deskripsi"))
    stock = strip_tags(request.POST.get("stock"))
    tanggal_akhir_berlaku = strip_tags(request.POST.get("tanggal_akhir_berlaku"))
    new_promo = Promo(
        nama=nama, kode=kode,
        potongan=potongan, deskripsi = deskripsi,
        stock = stock, tanggal_akhir_berlaku = tanggal_akhir_berlaku
    )
    new_promo.save()

    return HttpResponse(b"CREATED", status=201)

def show_xml(request):
    data = Promo.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, id):
    data = Promo.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    order_by = request.GET.get('order_by')
    urutan = request.GET.get('urutan') 
    param = order_by
    if urutan == "desc" :
        param = "-" + param
    data = Promo.objects.all().order_by(param)
    
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(id):
    data = Promo.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@admin_required
def view_promo_admin(request, id) :
    promo = Promo.objects.get(pk=id)
    context = {
        'promo' : promo,
    }
    return render(request, 'view_promo_admin.html', context)

@admin_required
def delete_promo(request, id) : 
    promo = Promo.objects.get(pk = id)
    promo.delete()
    return HttpResponseRedirect(reverse('promo:show_promo'))

@admin_required
def edit_promo(request, pk):
    promo = get_object_or_404(Promo, pk=pk)
    if request.method == 'POST':
        promo.nama = request.POST.get('nama')
        promo.kode = request.POST.get('kode')
        promo.potongan = request.POST.get('potongan')
        promo.tanggal_akhir_berlaku = request.POST.get('tanggal_akhir_berlaku')
        promo.stock = request.POST.get('stock')
        promo.deskripsi = request.POST.get('deskripsi')
        promo.save()
        return JsonResponse({'success': True})
    return render(request, 'edit_promo.html', {'promo': promo})