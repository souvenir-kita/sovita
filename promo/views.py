from django.shortcuts import render
from django.utils.html import strip_tags
from promo.models import Promo
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_promo(request):
    return render(request, "main_promo.html")

@csrf_exempt
@require_POST
def add_promo(request):
    nama = strip_tags(request.POST.get("nama"))
    kode = strip_tags(request.POST.get("kode"))
    potongan = strip_tags(request.POST.get("potongan"))
    deskripsi = strip_tags(request.POST.get("deskripsi"))
    stock = strip_tags(request.POST.get("stock"))
    new_promo = Promo(
        nama=nama, kode=kode,
        potongan=potongan, deskripsi = deskripsi,
        stock = stock
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
    data = Promo.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(id):
    data = Promo.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

