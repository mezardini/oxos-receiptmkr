from rest_framework.serializers import ModelSerializer
from .models import PdfFile, PdfFilepath, Business, ReceiptRequest
from django.contrib.auth.models import User
from rest_framework import serializers



class FileSerializer(ModelSerializer):
    class Meta:
        model = PdfFile
        fields = '__all__'

class FilepathSerializer(ModelSerializer):
    class Meta:
        model = PdfFilepath
        fields = '__all__'

class BusinessSerializer(ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class ReceiptRequestSerializer(ModelSerializer):
    class Meta:
        model = ReceiptRequest
        fields = '__all__'



class CartItemSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.DictField())
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
