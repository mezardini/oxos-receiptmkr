from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics, status, viewsets, renderers
from .serializers import  BusinessSerializer, CartItemSerializer, ReceiptRequestSerializer
from .models import PdfFile, PdfFilepath, Business, ReceiptRequest
from django.http import FileResponse
from rest_framework.decorators import action
import random
import jinja2
import pdfkit
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import F
from frontend.models import Seller, ReceiptDetails
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.template import loader, Template
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User, auth, Group
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa  



class CreatePDF(APIView):

    def post(self, request):
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data.get('name', '')
        token = json_data.get('token', '')
        business_name = json_data.get('name', '')
        customer_email = json_data.get('customer', '')
        business_url = json_data.get('website', '')
        user_no = token[-1]
        biz = Seller.objects.get(biz_code=token)
        seller = Seller.objects.get(user=user_no)
        seller_mail = seller.user.email
        allocation_quota = seller.receipt_allocation
        random_num = str(random.randint(11111,99999)) + str(user_no)
        if allocation_quota > 0:
        
            date = datetime.today().strftime("%d %b, %y")
            cart_items = request.POST.get('cartItems', {})
            cart_item_details = []
          

            # Access the cart items data and additional fields
            cart_items_data = json_data.get('cart_items', [])
            name = json_data.get('name', '')

            for cart_item in cart_items_data:
                quantity = cart_item['quantity']
                item_name = cart_item['itemName']
                item_price = cart_item['itemPrice']
                total_price = cart_item['totalPrice']

                # Perform any processing or database operations with the cart item data
                # Here, we're just appending the details to a list to be passed to the template
                cart_item_details.append({
                    'quantity': quantity,
                    'item_name': item_name,
                    'item_price': item_price,
                    'total_price': total_price
                })
            json_data = json.loads(request.body.decode('utf-8'))
            total_cart_price = sum(cart_item['totalPrice'] for cart_item in cart_items_data)

            context = { 'name':name, 'cart_item':cart_item_details, 'date':date, 'business_name':business_name, 
                       'business_url':business_url, 'total_cart_price':total_cart_price, 'random_num':random_num}
            
            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template('templates/newreceipt.html')
            output_text = template.render(context)

            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

            pdf_bytes = pdfkit.from_string(output_text, False, configuration=config, options={"enable-local-file-access": ""})

            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + name + '.pdf'
            serializer_class = ReceiptRequestSerializer
            data = {'receipt_name':name, 'user_no':token }
            serializer = ReceiptRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            
            seller = Seller.objects.filter(user=user_no).update(receipt_allocation=F('receipt_allocation') -1)
            
            return HttpResponse(response, content_type='application/pdf')
        
            
        else:
            
            # html_message = loader.render_to_string(
            #     'exceededemail.html',
            #     {
            #         'user_name': biz.user.username
            #     }

            #     )
                
            # mail = EmailMessage(
            #         "Registered",
            #         html_message,
            #         'settings.EMAIL_HOST_USER',
            #         [biz.user.email],
            #     )
            # mail.fail_silently = False
            # mail.content_subtype = 'html'
            # mail.send()
            return HttpResponse('Quota exceeded')


def sendReceipt(response, name):
    response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'
    return response

        