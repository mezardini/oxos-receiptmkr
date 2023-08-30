from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User, auth, Group
from .models import Seller, PaymentLogs, ReceiptDetails
from django.http import HttpResponse
import random
from django.contrib import messages
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template import loader, Template
from django.template.loader import render_to_string
from django.core import mail
from datetime import datetime, timedelta
from datetime import date
from django.conf import settings
from core_api.models import Business
from core_api.models import ReceiptRequest
import random
import string
from .services import create_seller_account

# Create your views here.



class Home(View): 
    template_name = 'index.html'
    # string = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8)))
    def get(self, request):
        # access_string = Home.string
        
        context = {}
        return render(request, 'index.html', context)
    def post(self, request):
        if request.method == 'POST':
            body = request.POST['message_body'],
            sender = request.POST['sender_email']
            mail = EmailMessage(
                    "Message from " + sender,
                    body,
                    'settings.EMAIL_HOST_USER',
                    ['mezardini@gmail.com'],
                )
            mail.fail_silently = False
            mail.content_subtype = 'html'
            mail.send()

def documentation(request):
    
    # access_string = Home.string 'access_string':access_string
        
    context = {}
    return render(request, 'api-doc.html', context)

def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

class Dashboard(LoginRequiredMixin, View):
    login_url = 'frontend:signup'  
    
    template_name = 'dashboard.html'
    
    def get(self, request ):
            
            if Seller.objects.filter(user=request.user.id).exists() :
                user = User.objects.get(id=request.user.id)
                biz = Seller.objects.get(user=user)
                receipts = ReceiptDetails.objects.filter(seller=biz)
                total_receipts = ReceiptRequest.objects.filter(user_no=biz.biz_code).count()
                specific_date = datetime(2023, 5, 29)  # Example: Year, Month, Day

                # Get the current date
                current_date = datetime.now()
                
                # Calculate the difference in days
                days_difference = (specific_date - current_date).days
                receipts_allocated = biz.receipt_allocation
                receipts_allocated_text = receipts_allocated
                if receipts_allocated > 100000:
                    receipts_allocated_text = 'Unlimited'

                
               
                    

                bar_width_1 = 5 #the value should be 0(zero) but i don't want the progress bar blank
                if total_receipts > 0:
                    bar_width_1 = (total_receipts/(total_receipts+receipts_allocated))*100
                bar_width_2 = (receipts_allocated/(total_receipts+receipts_allocated))*100

                context = {'user':user, 'biz':biz,  'total_receipts':total_receipts, 
                        'days_difference':days_difference, 'receipts_allocated':receipts_allocated_text, 
                        'bar_width_1':bar_width_1, 'bar_width_2':bar_width_2 ,'receipts':receipts }
                return render(request, 'dashboard.html', context)
            else:
                
                user = User.objects.get(id=request.user.id)
                biz_token = 'BC'+ str(random.randint(11111,99999)) + str(user.id)
                
                # users_in_group = Group.objects.get(name="Business").user_set.all()
                # if user not in users_in_group:
                seller_biz = Seller.objects.create(
                    user=user,
                    biz_code=biz_token
                )
                seller_biz.save()
                
                my_view = Dashboard()
                return my_view.get(request)
                


def signup(request):
   
    return render(request, 'sign-up.html')



def signout(request):
    logout(request)
    return redirect('frontend:signup') 

    

