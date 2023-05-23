from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics, status, viewsets, renderers
from .serializers import  BusinessSerializer, CartItemSerializer, ReceiptRequestSerializer
from .models import PdfFile, PdfFilepath, Business, ReceiptRequest
from django.http import FileResponse
from rest_framework.decorators import action
import jinja2
import pdfkit
from datetime import datetime
from django.core.mail import send_mail
from frontend.models import Seller
from rest_framework.decorators import api_view
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Create your views here.
# class makeReceipt(generics.CreateAPIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'templates/index.html'
#     def post(self, request):
#         code = request.POST['biz_id']
#         seller = Seller.objects.get(biz_code=code)
#         biz_name = seller.biz_name
#         biz_web = seller.web_url
#         name = request.POST['name']
#         product = request.POST['product']
#         price = request.POST['price']
#         date = datetime.today().strftime("%d %b, %y")

#         context = {'name':name, 'product':product, 'price':price, 'date':date, 'business_name':biz_name, 'business_website':biz_web}

#         template_loader = jinja2.FileSystemLoader('./')
#         template_env = jinja2.Environment(loader=template_loader)

#         template = template_env.get_template('pdftemplates/pdf4.html')
#         output_text = template.render(context)

#         path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#         config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#         filename = 'cv1.pdf'
#         pdfkit.from_string(output_text, 'pdfprint/'+filename, configuration=config, options={"enable-local-file-access": ""})
#         file_path = 'pdfprint/'+filename
#         FilePointer = open(file_path,"rb")
#         response = HttpResponse(FilePointer,content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'

#         return response
    
# class createBusiness(generics.CreateAPIView):
#     serializer_class = BusinessSerializer

#     def post(self, request, name, website, biz_code):
#         data = {'name':name, 'website': website, 'biz_code':biz_code }
#         serializer = BusinessSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class createReceipt(generics.CreateAPIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'templates/index.html'
#     def post(self, request, code, name, product, price):
#         # code = request.POST['biz_id']
#         seller = Seller.objects.get(biz_code=code)
#         biz_name = seller.biz_name
#         biz_web = seller.web_url
#         name = name
#         quantity = [2,1,5]
#         product = ['Samsung s23', 'Iphone 12 pro', 'Pixel 6a']
#         price = [450, 600, 800]
#         date = datetime.today().strftime("%d %b, %y")
#         Product = {
#             'product 1': {'Name': 'Samsung S23', 'price': 1300000, 'quantity': 2},
#             'product 2': {'Name': 'Iphone 12', 'price': 350000, 'quantity': 1},
#             'product 3': {'Name': 'PlayStation 5', 'price': 600000, 'quantity': 1},
#             'product 4': {'Name': 'Macbook Air', 'price': 1200000, 'quantity': 1},
#         }
#         total_price = sum(product["price"] for product in Product.values())

#         context = {'total_price':total_price, 'name':name, 'product':Product, 'quantity':quantity, 'price':price, 'date':date, 'business_name':biz_name, 'business_website':biz_web}

#         template_loader = jinja2.FileSystemLoader('./')
#         template_env = jinja2.Environment(loader=template_loader)

#         template = template_env.get_template('pdftemplates/pdf3.html')
#         output_text = template.render(context)

#         path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#         config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#         filename = 'cv1.pdf'
#         pdfkit.from_string(output_text, 'pdfprint/'+filename, configuration=config, options={"enable-local-file-access": ""})
#         file_path = 'pdfprint/'+filename
#         FilePointer = open(file_path,"rb")
#         response = HttpResponse(FilePointer,content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'

#         return HttpResponse('mezard')
    

# @csrf_exempt
# @api_view(['POST'])
# def cart(request):
#     serializer = CartItemSerializer(data=request.data)
#     if serializer.is_valid():
#         cart_items = serializer.validated_data['items']
#         total_price = serializer.validated_data['total_price']
#         # Loop through the cart items and print out the details
#         name = 'Olaoluwa'
        
#         context = {'total_price':total_price, 'name':name, 'product':cart_items}

#         template_loader = jinja2.FileSystemLoader('./')
#         template_env = jinja2.Environment(loader=template_loader)

#         template = template_env.get_template('pdftemplates/pdf4.html')
#         output_text = template.render(context)

#         path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#         config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#         filename = 'cv1.pdf'
#         pdfkit.from_string(output_text, 'pdfprint/'+filename, configuration=config, options={"enable-local-file-access": ""})
#         file_path = 'pdfprint/'+filename
#         FilePointer = open(file_path,"rb")
#         response['header-name'] = 'header-value'
#         response = HttpResponse(FilePointer,content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'

#         return response
#         # for item in cart_items:
#         #     item_name = item['name']
#         #     item_price = item['price']
#         #     item_quantity = item['quantity']
#         #     print(f"Item: {item_name}, Price: {item_price}, Quantity: {item_quantity}")
#         # # Process the cart item details here
#         # # ...
#         # return Response({'message': 'Cart items processed successfully.'})
#     else:
#         return Response(serializer.errors, status=400)












def download_pdf(request):
     if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data.get('name', '')
        token = json_data.get('token', '')
        business_name = json_data.get('website', '')
        customer_email = json_data.get('customer', '')
        business_url = json_data.get('customer', '')
        user_no = token[-1]
        # receiptrequest = ReceiptRequest.objects.create(
        #     receipt_name = name,
        #     user_no = user_no
        # )
        # receiptrequest.save()
        biz = Seller.objects.get(biz_code=token)
        # biz_name = biz.name
        receipt_quota = ReceiptRequest.objects.filter(user_no = token)
        quota = receipt_quota.count
        max_quota = 4
        if receipt_quota.count() <= 6:

            

        
            date = datetime.today().strftime("%d %b, %y")
            # name = 'Olaoluwa'
            cart_items = request.POST.get('cartItems', {})

            # Extract item details from the cart_items dictionary
            # cart_item_details = []
            # for cart_item in cart_items:
            #     quantity = cart_item.get('quantity')
            #     item_name = cart_item.get('itemName')
            #     item_price = cart_item.get('itemPrice')
            #     total_price = cart_item.get('totalPrice')
            #     cart_item_details.append({'quantity': quantity, 'item_name': item_name, 'item_price': item_price, 'total_price': total_price})
            # cart_items_data = json.loads(request.body)

            # # Query and process the cart items data
            cart_item_details = []
            # for cart_item in cart_items_data:
            #     quantity = cart_item['quantity']
            #     item_name = cart_item['itemName']
            #     item_price = cart_item['itemPrice']
            #     total_price = cart_item['totalPrice']

            #     # Perform any processing or database operations with the cart item data
            #     # Here, we're just appending the details to a list to be passed to the template
            #     cart_item_details.append({
            #         'quantity': quantity,
            #         'item_name': item_name,
            #         'item_price': item_price,
            #         'total_price': total_price
            #     })


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

            context = { 'name':name, 'cart_item':cart_item_details, 'date':date, 'business_name':business_name, 'business_url':business_url}
            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template('pdftemplates/pdf4.html')
            output_text = template.render(context)
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            filename = name+'.pdf'
            pdfkit.from_string(output_text, 'pdfprint/'+filename, configuration=config, options={"enable-local-file-access": ""})
            file_path = 'pdfprint/'+filename
            FilePointer = open(file_path,"rb")
            response = HttpResponse(FilePointer,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'
            serializer_class = ReceiptRequestSerializer
            data = {'receipt_name':name, 'user_no':token }
            serializer = ReceiptRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            email = EmailMessage(
                    'Here', 'Here is the message.', 'settings.EMAIL_HOST_USER', ['mezardini@gmail.com'])
            email.attach_file('pdfprint/'+name+'.pdf')
            email.send()

            return response
        
            
        else:
            send_mail(
            'Ticket booked!!!',
            'Quota exceeded',
            'settings.EMAIL_HOST_USER',
            ['ajisolaolaoluwa@gmail.com'],
            fail_silently=False,
            )
            return HttpResponse('Quota exceeded')
