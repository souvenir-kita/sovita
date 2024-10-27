from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from adminview.models import Product
from django.contrib.auth.models import User
import uuid

class ReviewEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Hanya menerima nilai 1-5
    description = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_entries')

