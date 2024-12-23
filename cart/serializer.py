from rest_framework import serializers
from .models import Cart, CartProduct

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'  # Includes cart, product, amount, note, and date_added


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'created_at']