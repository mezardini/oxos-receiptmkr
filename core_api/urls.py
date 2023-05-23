from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
# from .views import makeReceipt, createBusiness, createReceipt

urlpatterns = [
    # path("pdf", makeReceipt.as_view(), name="makeReceipt"),
    # path('createBiz/<str:name>/<str:website>/<str:biz_code>/', createBusiness.as_view(), name='createBiz'),
    # path("getpdf/<str:code>/<str:name>/<str:product>/<str:price>/", createReceipt.as_view(), name="createReceipt"),
    # path('cart/', views.cart, name='cart'),
    
    path('create_receipt/', csrf_exempt(views.download_pdf), name='download'),
]