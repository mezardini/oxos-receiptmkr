from django.test import TestCase

# Create your tests here.
import unittest
from .models import Seller, PaymentLogs
from django.contrib.auth.models import User



class SellerTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        
        user = User.objects.create_user(username='mezard', password='mezard2001')
        userx = User.objects.get(username='mezard')
        Seller.objects.create(biz_code='BC238929', user=userx, receipt_allocation=10)

    def test_your_model_method(self):
        obj = Seller.objects.get(biz_code='BC238929')

        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), obj.biz_code)
        print(obj.biz_code)

class PaymentLogTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        
        user = User.objects.create_user(username='mezard', password='mezard2001')
        userx = User.objects.get(username='mezard')
        PaymentLogs.objects.create(transaction_id='BC238929', payer=userx, amount=10, status='SUCCESS')

    def test_your_model_method(self):
        obj = PaymentLogs.objects.get(transaction_id='BC238929')

        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), f"{obj.payer.username} - {obj.amount}")

        print(f"{obj.payer.username} - {obj.amount}")