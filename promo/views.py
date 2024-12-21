import json
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
    user = request.user
    nama = strip_tags(request.POST.get("nama"))
    kode = strip_tags(request.POST.get("kode"))
    potongan = strip_tags(request.POST.get("potongan"))
    deskripsi = strip_tags(request.POST.get("deskripsi"))
    stock = strip_tags(request.POST.get("stock"))
    tanggal_akhir_berlaku = strip_tags(request.POST.get("tanggal_akhir_berlaku"))
    new_promo = Promo(
        nama=nama, kode=kode,
        potongan=potongan, deskripsi = deskripsi,
        stock = stock, tanggal_akhir_berlaku = tanggal_akhir_berlaku,
        user = user
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

def json_api(request):
    data = Promo.objects.all()

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

def show_json_by_kode(request, kode):
    data = Promo.objects.filter(kode=kode)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_promo_flutter(request):
    if request.method == 'POST':
        print(request.user)
        data = json.loads(request.body)
        new_promo = Promo.objects.create(
            user = request.user,
            kode = data["kode"],
            nama = data["nama"],
            potongan = int(data["potongan"]),
            stock = int(data["stock"]),
            deskripsi = data["deskripsi"],
            tanggal_akhir_berlaku = data["tanggal_akhir_berlaku"]
        )
        try:
            new_promo.save()
            print("SUKSES")
        except:
            print("FAIL")

        return JsonResponse({"status": "success"}, status=200)
    else:
        print("ERROR")
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_promo_flutter(request, pk) :
    if request.method == "POST" :
        data = json.loads(request.body)
        promo = Promo.objects.get(pk=pk)

        new_kode = data["kode"]
        new_nama = data["nama"]
        new_potongan = int(data["potongan"])
        new_stock = int(data["stock"])
        new_deskripsi = data["deskripsi"]
        new_tanggal_akhir_berlaku = data["tanggal_akhir_berlaku"]

        promo.nama = new_nama
        promo.kode = new_kode
        promo.potongan = new_potongan
        promo.stock = new_stock
        promo.deskripsi = new_deskripsi
        promo.tanggal_akhir_berlaku = new_tanggal_akhir_berlaku

        promo.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        
        return JsonResponse({"status": "error"}, status=401)
    

@csrf_exempt
def delete_promo_flutter(request, pk) :
    if request.method == "POST" :
        promo = Promo.objects.get(pk=pk)
        promo.delete()

        return JsonResponse({"status": "success"}, status=200)
    
    return JsonResponse({"status": "error"}, status=401)
