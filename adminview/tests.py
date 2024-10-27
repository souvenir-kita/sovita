from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import UserProfile
from adminview.models import Product
import datetime

class AdminAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testuser123'
        )
        UserProfile.objects.create(user=self.admin_user, role='admin')

        self.buyer_user = User.objects.create_user(
            username='buyer',
            password='pembeli123'
        )
        UserProfile.objects.create(user=self.buyer_user, role='buyer')

    def test_admin_login_redirect(self):
        response = self.client.post(reverse('authentication:login'), {
            'username': 'admin',
            'password': 'testuser123'
        })

        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('display:display_main'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.admin_user)

    def test_admin_access_to_admin_view(self):
        self.client.login(username='admin', password='testuser123')
        response_main = self.client.get(reverse('display:display_main'))
        self.assertEqual(response_main.status_code, 200)
        self.client.cookies['last_login'] = str(datetime.datetime.now())
        response_admin = self.client.get(reverse('adminview:show_admin'))
        self.assertEqual(response_admin.status_code, 200)

    def test_create_product_view(self):
        self.client.login(username='admin', password='testuser123')
        response_main = self.client.get(reverse('display:display_main'))
        self.assertEqual(response_main.status_code, 200)
        self.client.cookies['last_login'] = str(datetime.datetime.now())
        response_admin = self.client.get(reverse('adminview:show_admin'))
        self.assertEqual(response_admin.status_code, 200)

        product_data = {
            'name': 'New Product',
            'price': 15.00,
            'description': 'A brand new product',
            'category': 'New Category',
            'location': 'New Location',
        }
        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_non_admin_access(self):
        self.client.login(username='buyer', password='pembeli123')
        response_main = self.client.get(reverse('display:display_main'))
        self.assertEqual(response_main.status_code, 200)

        self.client.cookies['last_login'] = str(datetime.datetime.now())
        response_admin = self.client.get(reverse('adminview:show_admin'))
        self.assertEqual(response_admin.status_code, 403) 
    
    def test_edit_product(self):
        self.client.login(username='admin', password='testuser123')
        response_main = self.client.get(reverse('display:display_main'))
        self.assertEqual(response_main.status_code, 200)
        self.client.cookies['last_login'] = str(datetime.datetime.now())
        response_admin = self.client.get(reverse('adminview:show_admin'))
        self.assertEqual(response_admin.status_code, 200)

        product_data = {
            'name': 'New Product',
            'price': 15.00,
            'description': 'A brand new product',
            'category': 'New Category',
            'location': 'New Location',
        }

        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
        product_instance = Product.objects.get(name='New Product')

        updated_data = {
            'name': 'Updated Product',
            'price': 20.00,
            'description': 'An updated product',
            'category': 'Updated Category',
            'location': 'Updated Location',
        }

        response = self.client.post(reverse('adminview:edit_product', args=[product_instance.id]), data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminview:show_admin'))
        product_instance.refresh_from_db()
        self.assertEqual(product_instance.name, 'Updated Product')
        self.assertEqual(product_instance.price, 20.00)
        self.assertEqual(product_instance.description, 'An updated product')
        self.assertEqual(product_instance.category, 'Updated Category')
        self.assertEqual(product_instance.location, 'Updated Location')

    def test_delete_product(self):
        self.client.login(username='admin', password='testuser123')
        response_main = self.client.get(reverse('display:display_main'))
        self.assertEqual(response_main.status_code, 200)
        self.client.cookies['last_login'] = str(datetime.datetime.now())
        response_admin = self.client.get(reverse('adminview:show_admin'))
        self.assertEqual(response_admin.status_code, 200)

        product_data = {
            'name': 'New Product',
            'price': 15.00,
            'description': 'A brand new product',
            'category': 'New Category',
            'location': 'New Location',
        }
        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

        product_instance = Product.objects.get(name='New Product')
        response = self.client.post(reverse('adminview:delete_product', args=[product_instance.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminview:show_admin'))

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_instance.id)

    def test_show_json(self):
        self.client.login(username='admin', password='testuser123')
        product_data = {
            'name': 'Test Product',
            'price': 25.00,
            'description': 'A test product for JSON',
            'category': 'Test Category',
            'location': 'Test Location',
        }
        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        response_json = self.client.get(reverse('adminview:show_json'))
        self.assertEqual(response_json.status_code, 200)
        self.assertEqual(response_json['Content-Type'], 'application/json')
        json_data = response_json.content.decode('utf-8')
        self.assertIn('Test Product', json_data)

    def test_show_xml(self):
        self.client.login(username='admin', password='testuser123')
        product_data = {
            'name': 'Test Product',
            'price': 25.00,
            'description': 'A test product for XML',
            'category': 'Test Category',
            'location': 'Test Location',
        }
        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)

        response_xml = self.client.get(reverse('adminview:show_xml'))
        self.assertEqual(response_xml.status_code, 200)
        self.assertEqual(response_xml['Content-Type'], 'application/xml')
        xml_data = response_xml.content.decode('utf-8')

        self.assertIn('<field name="name" type="CharField">Test Product</field>', xml_data)


    def test_show_json_by_id(self):
        self.client.login(username='admin', password='testuser123')

        product_data = {
            'name': 'Test Product',
            'price': 25.00,
            'description': 'A test product for JSON by ID',
            'category': 'Test Category',
            'location': 'Test Location',
        }
        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)

        product_instance = Product.objects.get(name='Test Product')
        response_json_by_id = self.client.get(reverse('adminview:show_json_by_id', args=[product_instance.id]))
        self.assertEqual(response_json_by_id.status_code, 200)
        self.assertEqual(response_json_by_id['Content-Type'], 'application/json')
        json_data = response_json_by_id.content.decode('utf-8')
        self.assertIn('Test Product', json_data)

    def test_show_xml_by_id(self):
        self.client.login(username='admin', password='testuser123')

        product_data = {
            'name': 'Test Product',
            'price': 25.00,
            'description': 'A test product for XML by ID',
            'category': 'Test Category',
            'location': 'Test Location',
        }
        response = self.client.post(reverse('adminview:create_product_ajax'), data=product_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        product_instance = Product.objects.get(name='Test Product')
        response_xml_by_id = self.client.get(reverse('adminview:show_xml_by_id', args=[product_instance.id]))
        self.assertEqual(response_xml_by_id.status_code, 200)
        self.assertEqual(response_xml_by_id['Content-Type'], 'application/xml')
        xml_data = response_xml_by_id.content.decode('utf-8')
        self.assertIn('<field name="name" type="CharField">Test Product</field>', xml_data)