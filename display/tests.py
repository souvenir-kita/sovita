from django.test import TestCase, Client
from django.urls import reverse
from adminview.models import Product
from django.contrib.auth.models import User

class DisplayViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Sample Product', description='Sample Description', price=100)

    def test_display_main_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('display:display_main'))
        json_response = self.client.get(reverse('adminview:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display.html')
        self.assertContains(json_response, 'Sample Product')

    def test_display_main_view_unauthenticated(self):
        response = self.client.get(reverse('display:display_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'display.html')
        self.assertNotContains(response, 'last_login')

    def test_to_landing_view(self):
        response = self.client.get(reverse('display:to_landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_view_product(self):
        response = self.client.get(reverse('display:view_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_product.html')
        self.assertContains(response, 'Sample Product')

    def test_show_xml(self):
        response = self.client.get(reverse('display:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn(b'Sample Product', response.content)

    def test_show_json(self):
        response = self.client.get(reverse('display:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn(b'"name": "Sample Product"', response.content)

    def test_show_xml_by_id(self):
        response = self.client.get(reverse('display:show_xml_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn(b'<field name="name" type="CharField">Sample Product</field>', response.content)

    def test_show_json_by_id(self):
        response = self.client.get(reverse('display:show_json_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn(b'"name": "Sample Product"', response.content)

    def test_search_no_results(self):
        response = self.client.get(reverse('display:search'), {'searched': 'NonExistentProduct'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertNotContains(response, 'Sample Product')

    def test_search_with_results(self):
        response = self.client.get(reverse('display:search'), {'searched': 'Sample'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, 'Sample Product') 

#10 tests in here