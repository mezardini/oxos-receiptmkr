from django.contrib import admin
from .models import Seller, PaymentLogs, ReceiptDetails
# Register your models here.

admin.site.register(Seller)
admin.site.register(PaymentLogs)
admin.site.register(ReceiptDetails)