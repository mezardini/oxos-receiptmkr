from django.shortcuts import render
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
import jinja2
import pdfkit
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import F
from frontend.models import Seller
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.template import loader, Template
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User, auth, Group
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa  





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
        if receipt_quota.count() <= 3:

            

        
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
            template = template_env.get_template('pdftemplates/newreceipt.html')
            output_text = template.render(context)
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            filename = name+'.pdf'
            pdfkit.from_string(output_text, 'pdfprint/'+filename, configuration=config, options={"enable-local-file-access": ""})
            file_path = 'pdfprint/'+filename
            FilePointer = open(file_path,"rb")
            serializer_class = ReceiptRequestSerializer
            data = {'receipt_name':name, 'user_no':token }
            serializer = ReceiptRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            email = EmailMessage(
                    'Here', 'Here is the message.', 'settings.EMAIL_HOST_USER', ['mezardini@gmail.com'])
            email.attach_file('pdfprint/'+name+'.pdf')
            email.send()
            response = HttpResponse(FilePointer,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'
            return response
        
            
        else:
            # send_mail(
            # 'Notification: Exceeded Quota Limit',
            # 'Quota exceeded',
            # 'settings.EMAIL_HOST_USER',
            # ['ajisolaolaoluwa@gmail.com'],
            # fail_silently=False,
            # )
            reciever_name = biz.user.username
            reciever_mail = biz.user.email
            subject = 'Notification: Exceeded Quota Limit'
            message = 'Dear ' + reciever_name + ''',

            We hope this email finds you well. We wanted to bring to your attention that your allocated quota for Oxos-ReceiptMkr has been exceeded. We value your business and want to ensure that you have the best possible experience using our services.

            Here are the details regarding the exceeded quota:

            - Quota Type: Medium plan
            - Allocated Quota: 200

            As a result of exceeding the allocated quota, you may experience limitations or temporary service disruptions. To ensure uninterrupted access to our services, we kindly request that you take the necessary actions to address the exceeded quota.

            Here are some suggestions to manage your usage and avoid future quota limitations:

            1. Optimize Resource Usage: Review your current usage patterns and identify any inefficiencies or areas where resources could be optimized. Consider adjusting configurations or implementing best practices to optimize your resource utilization.

            2. Upgrade Quota: If you find that your current quota limit is consistently being exceeded, you may want to consider upgrading your quota to accommodate your growing needs. Please visit your Oxos dashboard to upgrade to a bigger plan.

            
            We are committed to providing you with the best possible service, and we appreciate your understanding and cooperation in addressing the exceeded quota. If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

            Thank you for choosing our services. We look forward to continuing to serve you and ensuring a seamless experience.

            Best regards,
            Mezard
            Oxos
            '''

            from_email = 'settings.EMAIL_HOST_USER'
            recipient_list = [reciever_mail]

            send_mail(subject, message, from_email, recipient_list)
            html_message = loader.render_to_string(
                'email.html',
                {
                    'user_name': biz.user.username
                    
                  
                }

                )
                # context = {'user_name': first_name,'token':   token}
                # template = template_env.get_template('templates/email.html')
                # output_text = template.render(context)
                # send_mail(
                #     'Ticket booked!!!',
                #      html_message,
                #     'tixvana@gmail.com',
                #     [email],
                #     fail_silently=False,
                # )
            mail = EmailMessage(
                    "Registered",
                    html_message,
                    'settings.EMAIL_HOST_USER',
                    [biz.user.email],
                )
            mail.fail_silently = False
            mail.content_subtype = 'html'
            mail.send()
            return HttpResponse('Quota exceeded')




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
        allocation_quota = seller.receipt_allocation
        # biz_name = biz.name
        if allocation_quota > 0:

            

        
            date = datetime.today().strftime("%d %b, %y")
            # name = 'Olaoluwa'
            cart_items = request.POST.get('cartItems', {})

        

            # # Query and process the cart items data
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

            context = { 'name':name, 'cart_item':cart_item_details, 'date':date, 'business_name':business_name, 'business_url':business_url}
            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template('pdftemplates/newreceipt.html')
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
                    'Purchase receipt', 'Here is your receipt.', 'ajisolaolaoluwa@gmail.com', ['mezardini@gmail.com'])
            email.attach_file('pdfprint/'+name+'.pdf')
            email.send()
            seller.update(receipt_allocation=F('receipt_allocation') -1 )
            
            return response
        
            
        else:
            # send_mail(
            # 'Notification: Exceeded Quota Limit',
            # 'Quota exceeded',
            # 'settings.EMAIL_HOST_USER',
            # ['ajisolaolaoluwa@gmail.com'],
            # fail_silently=False,
            # )
            # reciever_name = biz.user.username
            # reciever_mail = biz.user.email
            # subject = 'Notification: Exceeded Quota Limit'
            # message = 'Dear ' + reciever_name + ''',

            # We hope this email finds you well. We wanted to bring to your attention that your allocated quota for Oxos-ReceiptMkr has been exceeded. We value your business and want to ensure that you have the best possible experience using our services.

            # Here are the details regarding the exceeded quota:

            # - Quota Type: Medium plan
            # - Allocated Quota: 200

            # As a result of exceeding the allocated quota, you may experience limitations or temporary service disruptions. To ensure uninterrupted access to our services, we kindly request that you take the necessary actions to address the exceeded quota.

            # Here are some suggestions to manage your usage and avoid future quota limitations:

            # 1. Optimize Resource Usage: Review your current usage patterns and identify any inefficiencies or areas where resources could be optimized. Consider adjusting configurations or implementing best practices to optimize your resource utilization.

            # 2. Upgrade Quota: If you find that your current quota limit is consistently being exceeded, you may want to consider upgrading your quota to accommodate your growing needs. Please visit your Oxos dashboard to upgrade to a bigger plan.

            
            # We are committed to providing you with the best possible service, and we appreciate your understanding and cooperation in addressing the exceeded quota. If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

            # Thank you for choosing our services. We look forward to continuing to serve you and ensuring a seamless experience.

            # Best regards,
            # Mezard
            # Oxos
            # '''

            # from_email = 'settings.EMAIL_HOST_USER'
            # recipient_list = [reciever_mail]

            # send_mail(subject, message, from_email, recipient_list)
            html_message = loader.render_to_string(
                'exceededemail.html',
                {
                    'user_name': biz.user.username
                    
                  
                }

                )
                # context = {'user_name': first_name,'token':   token}
                # template = template_env.get_template('templates/email.html')
                # output_text = template.render(context)
                # send_mail(
                #     'Ticket booked!!!',
                #      html_message,
                #     'tixvana@gmail.com',
                #     [email],
                #     fail_silently=False,
                # )
            mail = EmailMessage(
                    "Registered",
                    html_message,
                    'settings.EMAIL_HOST_USER',
                    [biz.user.email],
                )
            mail.fail_silently = False
            mail.content_subtype = 'html'
            mail.send()
            return HttpResponse('Quota exceeded')

        