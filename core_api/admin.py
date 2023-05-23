from django.contrib import admin
from .models import PdfFile, PdfFilepath, Business, ReceiptRequest

# Register your models here.
admin.site.register(PdfFile)
admin.site.register(PdfFilepath)
admin.site.register(Business)
admin.site.register(ReceiptRequest)