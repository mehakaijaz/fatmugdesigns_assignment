
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.utils import timezone

class VendorAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.vendor_data = {'name': 'Test Vendor', 'contact_details': 'Contact Info', 'address': 'Vendor Address', 'vendor_code': 'V001'}

    def test_create_vendor(self):
        response = self.client.post(reverse('vendor-list-create'), self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)

    def test_get_vendors(self):
        Vendor.objects.create(name='Vendor1', contact_details='Contact1', address='Address1', vendor_code='V001')
        Vendor.objects.create(name='Vendor2', contact_details='Contact2', address='Address2', vendor_code='V002')
        response = self.client.get(reverse('vendor-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_vendor(self):
        vendor = Vendor.objects.create(name='VendorToUpdate', contact_details='ContactToUpdate', address='AddressToUpdate', vendor_code='V003')
        updated_data = {'name': 'UpdatedVendor', 'contact_details': 'UpdatedContact', 'address': 'UpdatedAddress', 'vendor_code': 'V003'}
        response = self.client.put(reverse('vendor-retrieve-update-delete', args=[vendor.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vendor.refresh_from_db()
        self.assertEqual(vendor.name, 'UpdatedVendor')

    def test_delete_vendor(self):
        vendor = Vendor.objects.create(name='VendorToDelete', contact_details='ContactToDelete', address='AddressToDelete', vendor_code='V004')
        response = self.client.delete(reverse('vendor-retrieve-update-delete', args=[vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Vendor Address', vendor_code='V001')
        self.purchase_order_data = {'po_number': 'PO001', 'vendor': self.vendor.id, 'order_date': '2023-01-01T00:00:00Z', 'delivery_date': '2023-01-10T00:00:00Z', 'items': {'item1': 'Description1'}, 'quantity': 10, 'status': 'pending'}

    def test_create_purchase_order(self):
        response = self.client.post(reverse('purchase-order-list-create'), self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)

    def test_get_purchase_orders(self):
        PurchaseOrder.objects.create(po_number='PO001', vendor=self.vendor, order_date='2023-01-01T00:00:00Z', delivery_date='2023-01-10T00:00:00Z', items={'item1': 'Description1'}, quantity=10, status='completed')
        PurchaseOrder.objects.create(po_number='PO002', vendor=self.vendor, order_date='2023-01-02T00:00:00Z', delivery_date='2023-01-12T00:00:00Z', items={'item2': 'Description2'}, quantity=20, status='pending')
        response = self.client.get(reverse('purchase-order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


    def test_update_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(
            po_number='PO003',
            vendor=self.vendor,
            order_date='2023-01-03T00:00:00Z',
            delivery_date='2023-01-15T00:00:00Z',
            items={'item3': 'Description3'},
            quantity=15,
            status='pending'
        )
        updated_data = {
            'po_number': 'PO003',
            'vendor': self.vendor.id,
            'order_date': '2023-01-03T00:00:00Z',
            'delivery_date': '2023-01-20T00:00:00Z',
            'items': {'item3': 'UpdatedDescription3'},
            'quantity': 20,
            'status': 'completed'
        }
        response = self.client.put(
            reverse('purchase-order-retrieve-update-delete', args=[purchase_order.id]),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_order.refresh_from_db()
        
        # Convert the string to a datetime object for comparison
        expected_delivery_date = datetime.strptime('2023-01-20T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        
        self.assertEqual(purchase_order.delivery_date, expected_delivery_date)


    def test_delete_purchase_order(self):
        purchase_order = PurchaseOrder.objects.create(po_number='PO004', vendor=self.vendor, order_date='2023-01-04T00:00:00Z', delivery_date='2023-01-18T00:00:00Z', items={'item4': 'Description4'}, quantity=18, status='pending')
        response = self.client.delete(reverse('purchase-order-retrieve-update-delete', args=[purchase_order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)


class HistoricalPerformanceAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact Info', address='Vendor Address', vendor_code='V001')
        self.historical_performance_data = {
            'vendor': self.vendor.id,
            'date': '2023-01-15T00:00:00Z',
            'on_time_delivery_rate': 90.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 24.5,
            'fulfillment_rate': 95.0,
        }

    def test_create_historical_performance(self):
        response = self.client.post(reverse('historical-performance-list-create'), self.historical_performance_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HistoricalPerformance.objects.count(), 1)

    def test_get_historical_performances(self):
        HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date='2023-01-15T00:00:00Z',
            on_time_delivery_rate=90.0,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=95.0,
        )
        HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date='2023-01-16T00:00:00Z',
            on_time_delivery_rate=85.0,
            quality_rating_avg=4.0,
            average_response_time=26.0,
            fulfillment_rate=92.0,
        )
        response = self.client.get(reverse('historical-performance-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_historical_performance(self):
        historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date='2023-01-15T00:00:00Z',
            on_time_delivery_rate=90.0,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=95.0,
        )
        updated_data = {
            'vendor': self.vendor.id,
            'date': '2023-01-15T00:00:00Z',
            'on_time_delivery_rate': 92.0,
            'quality_rating_avg': 4.8,
            'average_response_time': 23.0,
            'fulfillment_rate': 97.0,
        }
        response = self.client.put(
            reverse('historical-performance-retrieve-update-delete', args=[historical_performance.id]),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        historical_performance.refresh_from_db()
        self.assertEqual(historical_performance.on_time_delivery_rate, 92.0)

    def test_delete_historical_performance(self):
        historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date='2023-01-15T00:00:00Z',
            on_time_delivery_rate=90.0,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=95.0,
        )
        response = self.client.delete(reverse('historical-performance-retrieve-update-delete', args=[historical_performance.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HistoricalPerformance.objects.count(), 0)


class PurchaseOrderAcknowledgeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.vendor = Vendor.objects.create(name='Vendor Test', contact_details='Contact Test', address='Address Test', vendor_code='V001')
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date='2023-01-01T00:00:00Z',
            delivery_date='2023-01-10T00:00:00Z',
            items={'item': 'Test'},
            quantity=10,
            status='pending',
            issue_date='2023-01-02T00:00:00Z',
        )
        self.url = reverse('purchase-order-acknowledge', args=[self.purchase_order.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_acknowledge_purchase_order(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)
        self.vendor.refresh_from_db()
        self.assertIsNotNone(self.vendor.average_response_time)
