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
from .serializers import BusinessSerializer, CartItemSerializer, ReceiptRequestSerializer
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
        try:
            # Parse JSON data from the request body
            json_data = json.loads(request.body.decode('utf-8'))
            name = json_data.get('name', '')
            token = json_data.get('token', '')
            business_name = json_data.get('name', '')
            customer_email = json_data.get('customer', '')
            business_url = json_data.get('website', '')

            # Extract user_no from token
            user_no = token[-1]

            # Retrieve seller and verify quota
            seller = get_object_or_404(Seller, biz_code=token, user=user_no)
            allocation_quota = seller.receipt_allocation

            if allocation_quota <= 0:
                return HttpResponse('Quota exceeded')

            # Extract cart items data
            cart_items_data = json_data.get('cart_items', [])
            total_cart_price = sum(cart_item['totalPrice']
                                   for cart_item in cart_items_data)

            receipt_id = str(random.randint(11111, 99999)) + str(user_no)
            # Prepare context for the PDF template
            context = {
                'name': name,
                'cart_item_details': cart_items_data,
                'date': datetime.today().strftime("%d %b, %y"),
                'business_name': business_name,
                'business_url': business_url,
                'total_cart_price': total_cart_price,
                'random_num': receipt_id,
            }

            template = loader.get_template('templates/newreceipt.html')
            output_text = template.render(context)

            # Create a PDF file
            pdf_file = open('output.pdf', 'wb')
            pisa_status = pisa.CreatePDF(output_text, dest=pdf_file)

            # Close the PDF file
            pdf_file.close()

            # Check if PDF creation was successful
            if pisa_status.err:
                return HttpResponse('PDF generation failed!', content_type='text/plain')

            # Prepare PDF response
            with open('output.pdf', 'rb') as pdf_file:
                response = HttpResponse(
                    pdf_file.read(), content_type='application/pdf')

            response['Content-Disposition'] = 'attachment; filename=' + \
                name+receipt_id + '.pdf'

            # Save a record of the receipt request
            data = {'receipt_name': name, 'user_no': token}
            serializer = ReceiptRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

            # Update seller's receipt_allocation
            seller.receipt_allocation -= 1
            seller.save()

            return response

        except Exception as e:
            return Response({'error': str(e)})


def sendReceipt(response, name):
    response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'
    return response
