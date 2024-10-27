from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from authentication.models import UserProfile
from .models import Cart, Product

User = get_user_model()

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/skibidi/')
        self.assertEqual(response.status_code, 404)
        
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='qwerqwer12')
        
        # Create a UserProfile for the user
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role='buyer',
            address='123 Main St',
            age=30,
            phone_number='1234567890'
        )
        
        self.client.login(username='testuser', password='qwerqwer12')
        
        # Create a product for testing
        self.product = Product.objects.create(name='Test Product', price=10.0)
        
        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)