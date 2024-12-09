from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
import datetime
import uuid

class Promo(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    kode = models.CharField(unique= True, max_length= 15, validators=[MinLengthValidator(4)])
    nama = models.CharField(max_length=20)
    potongan = models.IntegerField(max_length=100, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    deskripsi = models.TextField()
    tanggal_akhir_berlaku = models.DateField()