
from django.db import models
from django.contrib.auth.models import User
from adminview.models import Product

class Wishlist(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    added_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=2)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (Priority {self.priority})"