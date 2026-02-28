from decimal import Decimal
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.inventory.models import Category, Item, Store, StoreItem


CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


@override_settings(CHANNEL_LAYERS=CHANNEL_LAYERS)
class BarcodeScanTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='inv_user', password='testpass123')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Medical Supplies')
        self.item = Item.objects.create(
            name='Syringe 5ml',
            barcode='INV-12345',
            category=self.category,
            unit='pieces',
            created_by=self.user,
        )
        self.store = Store.objects.create(name='Main Store', store_type='main')
        self.store_item = StoreItem.objects.create(
            store=self.store,
            item=self.item,
            quantity=Decimal('100.00'),
            unit_cost=Decimal('5.00'),
        )

    def test_successful_barcode_scan(self):
        resp = self.client.post('/api/v1/inventory/barcode-scan/', {
            'barcode': 'INV-12345',
            'store': str(self.store.id),
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['quantity_removed'], 1)
        self.store_item.refresh_from_db()
        self.assertEqual(self.store_item.quantity, Decimal('99.00'))

    def test_scan_custom_quantity(self):
        resp = self.client.post('/api/v1/inventory/barcode-scan/', {
            'barcode': 'INV-12345',
            'store': str(self.store.id),
            'quantity': 10,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['quantity_removed'], 10)
        self.store_item.refresh_from_db()
        self.assertEqual(self.store_item.quantity, Decimal('90.00'))

    def test_scan_unknown_barcode(self):
        resp = self.client.post('/api/v1/inventory/barcode-scan/', {
            'barcode': 'UNKNOWN-999',
            'store': str(self.store.id),
        })
        self.assertEqual(resp.status_code, 404)

    def test_scan_missing_barcode(self):
        resp = self.client.post('/api/v1/inventory/barcode-scan/', {
            'store': str(self.store.id),
        })
        self.assertEqual(resp.status_code, 400)

    def test_scan_missing_store(self):
        resp = self.client.post('/api/v1/inventory/barcode-scan/', {
            'barcode': 'INV-12345',
        })
        self.assertEqual(resp.status_code, 400)

    def test_scan_insufficient_stock(self):
        self.store_item.quantity = Decimal('0')
        self.store_item.save()
        resp = self.client.post('/api/v1/inventory/barcode-scan/', {
            'barcode': 'INV-12345',
            'store': str(self.store.id),
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Insufficient stock', resp.data['detail'])

    def test_scan_requires_auth(self):
        client = APIClient()
        resp = client.post('/api/v1/inventory/barcode-scan/', {
            'barcode': 'INV-12345',
            'store': str(self.store.id),
        })
        self.assertEqual(resp.status_code, 401)
