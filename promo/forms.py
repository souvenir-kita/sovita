from django.forms import ModelForm
from promo.models import Promo

class ProductForm(ModelForm):
    class Meta:
        model = Promo
        fields = ["nama", "kode", "potongan", "deskripsi", "tanggal_akhir_berlaku"]