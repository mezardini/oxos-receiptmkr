from django.contrib import admin
from django.urls import path
from .views import CreatePDF
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
# from .views import makeReceipt, createBusiness, createReceipt

urlpatterns = [
    path('create_pdf/', CreatePDF.as_view(), name='create_pdf'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)