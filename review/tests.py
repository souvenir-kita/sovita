# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from review.models import ReviewEntry, Product
import pytz
from django.utils import timezone
from authentication.models import UserProfile

class SimpleReviewTests(TestCase):
    def setUp(self):
        # Set up client, user, and product for testing
        self.client = Client()
        self.buyer = User.objects.create_user(username='buyer', password='testpass')
        
        # Tambahkan userprofile untuk buyer dan set role sebagai 'buyer'
        self.buyer.userprofile = UserProfile.objects.create(user=self.buyer, role='buyer')
        
        # Buat produk dengan harga yang memenuhi syarat NOT NULL
        self.product = Product.objects.create(name='Sample Product', price=10000)
        
        # Buat review contoh
        self.review = ReviewEntry.objects.create(
            user=self.buyer,
            product=self.product,
            rating=4,
            deskripsi="Good product",
            date_create=timezone.now()
        )

    def test_create_review_as_buyer(self):
        # Test if a buyer can create a review successfully
        self.client.login(username='buyer', password='testpass')
        response = self.client.post(reverse('review:create_review', args=[self.product.id]), {
            'rating': 5,
            'deskripsi': 'Amazing product!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ReviewEntry.objects.filter(deskripsi='Amazing product!').exists())

    def test_show_review_page_status_code(self):
        # Test if show_review page returns a 200 status code
        self.client.login(username='buyer', password='testpass')
        response = self.client.get(reverse('review:show_review', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)


    def test_edit_review_as_owner(self):
        # Test if the owner of a review can edit it successfully
        self.client.login(username='buyer', password='testpass')
        response = self.client.post(reverse('review:edit_review', args=[self.review.id]), {
            'rating': 3,
            'deskripsi': 'Updated description'
        })
        self.review.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(self.review.deskripsi, 'Updated description')

    def test_delete_review_as_owner(self):
        # Test if the owner of a review can delete it successfully
        self.client.login(username='buyer', password='testpass')
        response = self.client.post(reverse('review:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(ReviewEntry.objects.filter(id=self.review.id).exists())

    def test_show_json_response(self):
        # Test if show_json returns a JSON response with the correct data
        response = self.client.get(reverse('review:show_json', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['fields']['deskripsi'], 'Good product')
