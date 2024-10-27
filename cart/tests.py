from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from authentication.models import UserProfile
from .models import Cart, Product, CartProduct
from django.urls import reverse
import json

User = get_user_model()


class mainTest(TestCase):
    def test_cart_url_is_exist(self):
        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_cart.html')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.product = Product.objects.create(name='Sample Product', description='Sample Description', price=100)
        self.another_product = Product.objects.create(name='Another Product', description='Another Description', price=50)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_product = CartProduct.objects.create(cart=self.cart, product=self.product, amount=1)
    
    def test_show_cart_template_used(self):
        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_cart.html')
        
    def test_show_cart_context_data(self):
        response = self.client.get(reverse('cart:show_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['cart'], self.cart)
        self.assertIn(self.cart_product, response.context['cart_products'])
        self.assertEqual(response.context['current_sort'], 'alphabet_asc')
    
    def test_show_cart_sorting(self):
        another_product = Product.objects.create(name='Another Product', description='Another Description', price=50)
        another_cart_product = CartProduct.objects.create(cart=self.cart, product=another_product, amount=1)
        response = self.client.get(reverse('cart:show_cart'), {'sort': 'alphabet_asc'})
        self.assertEqual(response.context['cart_products'][0].product.name, 'Another Product')
        response = self.client.get(reverse('cart:show_cart'), {'sort': 'alphabet_dsc'})
        self.assertEqual(response.context['cart_products'][0].product.name, 'Sample Product')
    
    def test_add_product_to_cart(self):
        response = self.client.post(reverse('cart:add_product_to_cart', args=[self.product.id]), {
            'cart_amount': 2
        })
        self.assertEqual(response.status_code, 302)
        cart_product = CartProduct.objects.filter(cart=self.cart, product=self.product).first()
        self.assertIsNotNone(cart_product)
        self.assertEqual(cart_product.amount, 3)
        


    