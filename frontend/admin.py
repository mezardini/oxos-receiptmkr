from django.contrib import admin
from .models import Seller, PaymentLogs
# Register your models here.

admin.site.register(Seller)
admin.site.register(PaymentLogs)