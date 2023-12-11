import json
import random
from datetime import datetime
from io import BytesIO
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import Seller  # Import your Seller model
from .serializers import ReceiptRequestSerializer  # Import your serializer
import xhtml2pdf.pisa as pisa


class CreatePDF(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user'  # Use 'user' scope for authenticated users

    def post(self, request):
        try:
            # Parse JSON data from the request body
            json_data = json.loads(request.body.decode('utf-8'))
            name = json_data.get('name', '')
            token = json_data.get('token', '')
            business_name = json_data.get(
                'business_name', '')  # Fix the field name
            customer_email = json_data.get('customer', '')
            business_url = json_data.get('website', '')

            # Extract user_no from token
            user_no = int(token[-1])  # Convert to integer

            # Retrieve seller and verify quota
            seller = get_object_or_404(Seller, biz_code=token, user=user_no)
            allocation_quota = seller.receipt_allocation

            if allocation_quota <= 0:
                # Return 429 for rate limiting
                return HttpResponse('Quota exceeded', status=429)

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

            # Create a PDF in-memory
            pdf_buffer = BytesIO()
            pisa.CreatePDF(output_text, dest=pdf_buffer)

            # Prepare PDF response
            pdf_buffer.seek(0)
            response = HttpResponse(
                pdf_buffer.read(), content_type='application/pdf')

            response['Content-Disposition'] = 'attachment; filename=' + \
                name + receipt_id + '.pdf'

            # Save a record of the receipt request
            data = {'receipt_name': name, 'user_no': user_no}
            serializer = ReceiptRequestSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

            # Update seller's receipt_allocation
            seller.receipt_allocation -= 1
            seller.save()

            return response

        except Exception as e:
            # Return 500 for internal server error
            return Response({'error': str(e)}, status=500)
