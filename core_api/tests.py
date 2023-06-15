from django.test import TestCase

# Create your tests here.
import unittest
from .models import ReceiptRequest
from django.contrib.auth.models import User


class ReceiptRequestTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        
        ReceiptRequest.objects.create(receipt_name='mezard', user_no=9)

    def test_your_model_method(self):
        obj = ReceiptRequest.objects.get(receipt_name='mezard')
        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), 'mezard by 9')

class ReceiptRequestTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        
        ReceiptRequest.objects.create(receipt_name='mezard', user_no=9)

    def test_your_model_method(self):
        obj = ReceiptRequest.objects.get(receipt_name='mezard')
        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), 'mezard by 9')