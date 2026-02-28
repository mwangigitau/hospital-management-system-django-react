from datetime import date, timedelta
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.pharmacy.models import Drug, DrugBatch, StockMovement


CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


@override_settings(CHANNEL_LAYERS=CHANNEL_LAYERS)
class PharmacyBarcodeScanTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='pharm_user', password='testpass123')
        self.client.force_authenticate(user=self.user)

        self.drug = Drug.objects.create(
            name='Paracetamol 500mg',
            barcode='DRUG-67890',
            generic_name='Paracetamol',
            category='analgesic',
            unit='tablets',
            created_by=self.user,
        )
        self.batch = DrugBatch.objects.create(
            drug=self.drug,
            batch_number='B001',
            expiry_date=date.today() + timedelta(days=365),
            quantity=200,
            purchase_price='2.00',
            selling_price='5.00',
        )

    def test_successful_barcode_scan(self):
        resp = self.client.post('/api/v1/pharmacy/barcode-scan/', {
            'barcode': 'DRUG-67890',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['quantity_dispensed'], 1)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity, 199)
        self.assertEqual(StockMovement.objects.count(), 1)
        movement = StockMovement.objects.first()
        self.assertEqual(movement.movement_type, 'out')
        self.assertEqual(movement.quantity, 1)

    def test_scan_custom_quantity(self):
        resp = self.client.post('/api/v1/pharmacy/barcode-scan/', {
            'barcode': 'DRUG-67890',
            'quantity': 5,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['quantity_dispensed'], 5)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity, 195)

    def test_scan_unknown_barcode(self):
        resp = self.client.post('/api/v1/pharmacy/barcode-scan/', {
            'barcode': 'UNKNOWN-999',
        })
        self.assertEqual(resp.status_code, 404)

    def test_scan_missing_barcode(self):
        resp = self.client.post('/api/v1/pharmacy/barcode-scan/', {})
        self.assertEqual(resp.status_code, 400)

    def test_scan_insufficient_stock(self):
        self.batch.quantity = 0
        self.batch.save()
        resp = self.client.post('/api/v1/pharmacy/barcode-scan/', {
            'barcode': 'DRUG-67890',
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Insufficient stock', resp.data['detail'])

    def test_scan_uses_fefo(self):
        """Earliest-expiring batch should be used first."""
        early_batch = DrugBatch.objects.create(
            drug=self.drug,
            batch_number='B-EARLY',
            expiry_date=date.today() + timedelta(days=30),
            quantity=50,
            purchase_price='2.00',
            selling_price='5.00',
        )
        resp = self.client.post('/api/v1/pharmacy/barcode-scan/', {
            'barcode': 'DRUG-67890',
        })
        self.assertEqual(resp.status_code, 200)
        early_batch.refresh_from_db()
        self.assertEqual(early_batch.quantity, 49)

    def test_scan_requires_auth(self):
        client = APIClient()
        resp = client.post('/api/v1/pharmacy/barcode-scan/', {
            'barcode': 'DRUG-67890',
        })
        self.assertEqual(resp.status_code, 401)
