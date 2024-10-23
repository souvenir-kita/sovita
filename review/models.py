from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from display.models import Product
from django.contrib.auth.models import User
import uuid

class ReviewEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    description = models.TextField()
    date_create = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_entries')

