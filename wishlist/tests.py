from django.test import TestCase
from django.contrib.auth.models import User
from adminview.models import Product
from .models import Wishlist
from django.urls import reverse

class WishlistTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', price=100)
        self.client.login(username='testuser', password='password')

    def test_add_to_wishlist(self):
        wishlist_item = Wishlist.objects.create(user=self.user, product=self.product, priority=2)
        self.assertEqual(Wishlist.objects.count(), 1)
        self.assertEqual(wishlist_item.user, self.user)
        self.assertEqual(wishlist_item.product, self.product)

    def test_toggle_wishlist(self):
        self.client.post(reverse('wishlist:toggle_wishlist', args=[self.product.id]), content_type="application/json", data={})
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())
        self.client.post(reverse('wishlist:toggle_wishlist', args=[self.product.id]), content_type="application/json", data={})
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_access_wishlist_page(self):
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')
        self.assertContains(response, 'Your Wishlist')

    def test_access_non_existent_page(self):
        response = self.client.get('/wishlist/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def test_priority_filter_in_wishlist(self):
        Wishlist.objects.create(user=self.user, product=self.product, priority=1)
        response = self.client.get(reverse('wishlist:show_wishlist'), {'priority': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Low')