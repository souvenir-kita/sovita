from django.db import models
from django.core.validators import MinValueValidator
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    description = models.TextField()
    picture = models.ImageField(upload_to='img/', default='img/default.png') 
    location = models.CharField(max_length=255)
    shop = models.CharField(max_length=255)
