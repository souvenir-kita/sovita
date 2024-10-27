from django.test import TestCase, Client
from django.urls import reverse
from promo.models import Promo
from datetime import datetime, timedelta
import json

class PromoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.test_promo = Promo.objects.create(
            nama="Test Promo",
            kode="TESTCODE",
            potongan="10000",
            deskripsi="Test Description",
            stock=100,
            tanggal_akhir_berlaku=datetime.now().date() + timedelta(days=30)
        )

    def test_show_json_by_kode(self):
        response = self.client.get(reverse('promo:show_json_by_kode', args=["TESTCODE"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        response = self.client.get(reverse('promo:show_json_by_kode', args=["NONEXISTENT"]))
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_add_promo(self):
        promo_data = {
            'nama': 'New Test Promo',
            'kode': 'NEWCODE',
            'potongan': '20000',
            'deskripsi': 'New Test Description',
            'stock': '50',
            'tanggal_akhir_berlaku': (datetime.now().date() + timedelta(days=30)).strftime('%Y-%m-%d')
        }
        
        response = self.client.post(reverse('promo:add_promo'), promo_data)
        self.assertEqual(response.status_code, 403)

    def test_edit_promo(self):
        updated_data = {
            'nama': 'PUSINGPBP',
            'kode': 'UPDATEDCODE',
            'potongan': '30000',
            'deskripsi': 'Updated Description',
            'stock': '75',
            'tanggal_akhir_berlaku': (datetime.now().date() + timedelta(days=60)).strftime('%Y-%m-%d')
        }
        
        response = self.client.post(
            reverse('promo:edit_promo', args=[self.test_promo.id]), 
            updated_data
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_promo(self):
        response = self.client.post(reverse('promo:delete_promo', args=[self.test_promo.id]))

        self.assertEqual(response.status_code, 403)

    def test_view_promo_admin(self):
        response = self.client.get(reverse('promo:view_promo_admin', args=[self.test_promo.id]))

        self.assertEqual(response.status_code, 403)