import uuid
from django.db import models
from adminview.models import Product

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    amount = models.PositiveIntegerField()
    note = models.TextField(max_length=144, blank=True, null=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.amount} of {self.product.name} in {self.cart}"

    def total_price(self):
        return self.amount * self.product.price
