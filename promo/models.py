from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
import datetime
import uuid

class Promo(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kode = models.CharField(unique= True, max_length= 15, validators=[MinLengthValidator(4)])
    nama = models.CharField(max_length=100)
    potongan = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    deskripsi = models.TextField()
    tanggal_akhir_berlaku = models.DateField()