from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User, auth, Group
from .models import Seller, PaymentLogs
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


# Create your views here.



class Home(View): 
    template_name = 'index.html'
    string = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8)))
    def get(self, request):
        access_string = Home.string
        
        context = {'access_string':access_string}
        return render(request, 'index.html', context)

def documentation(request):
    
    access_string = Home.string
        
    context = {'access_string':access_string}
    return render(request, 'api-doc.html', context)

def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

class Dashboard(LoginRequiredMixin, View):
    login_url = 'frontend:home'  
    
    template_name = 'dashboard.html'
    
    def get(self, request ):
        
            user = User.objects.get(id=request.user.id)
            if request.user == user:
                biz_token = 'BC'+ str(random.randint(11111,99999)) + str(user.id)
                

                users_in_group = Group.objects.get(name="Business").user_set.all()
                if user not in users_in_group :
                    seller_biz = Seller.objects.create(
                        user = user,
                        biz_code = biz_token
                    )
                    seller_biz.save()
                    user_group = Group.objects.get(name="Business")
                    user.groups.add(user_group)
                
                    # biz = Business.objects.create(
                    #     name = request.POST['biz_name'],
                    #     website = request.POST['web_url'],
                    #     biz_code = biz_token+str(user.pk),
                    #     text = request.POST['additional_text'],
                    #     template = request.POST['template_choice'],
                    #     user_no = user.pk
                    # )
                    # biz.save()
                biz = Seller.objects.get(user=user)
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

                
                user_plan_and_text = {'Free':'You are on free plan, your plan expires on 20th June, 2023','Basic':'You are on basic plan, your plan expires on 20th June, 2023', 'Medium':'You are on medium plan, your plan expires on 20th June, 2023', 'Large':'You are on Enterprise plan, your plan expires on 20th June, 2023' }
                subscription_text = 'You are on free trial, your plan expires on 20th June, 2023'
                users_in_freegroup = Group.objects.get(name="Free tier").user_set.all()
                users_in_group = Group.objects.get(name="Business").user_set.all()
                users_in_group3 = Group.objects.get(name="Large").user_set.all()
                users_in_group2 = Group.objects.get(name="Medium").user_set.all()
                if user in users_in_freegroup:
                    subscription_text = user_plan_and_text['Free']
                    
                elif user in users_in_group:
                    subscription_text = user_plan_and_text['Basic']
                    

                elif user in users_in_group2:
                    subscription_text = user_plan_and_text['Medium']
                    
                
                elif user in users_in_group3:
                    subscription_text = user_plan_and_text['Large']
                    

                bar_width_1 = 5 #the value should be 0(zero) but i don't want the progress bar blank
                if total_receipts > 0:
                    bar_width_1 = (total_receipts/(total_receipts+receipts_allocated))*100
                bar_width_2 = (receipts_allocated/(total_receipts+receipts_allocated))*100

                context = {'user':user, 'biz':biz, 'text':subscription_text, 'total_receipts':total_receipts, 
                        'days_difference':days_difference, 'receipts_allocated':receipts_allocated_text, 'bar_width_1':bar_width_1, 'bar_width_2':bar_width_2  }
                return render(request, 'dashboard.html', context)
            else:
                return redirect('frontend:home')
        
        
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        base_5 = 'Basic'
        base_10 = 'Medium'
        base_25 = 'Large'
        current_date = date.today()
        allocation = 50

        if request.method == 'POST':
            if request.POST['template_choice'] == 'silver':
                allocation = 150
                return redirect('https://business.quickteller.com/link/pay/oxos')
            elif request.POST['template_choice'] == 'gold':
                allocation = 500
                return redirect('https://business.quickteller.com/link/pay/tixvanaUKxsv')
            elif request.POST['template_choice'] == 'platinum':
                allocation = 1500
            # return redirect('https://business.quickteller.com/link/pay/tixvanaUKxsv')
            
        


def signup(request):
    global user
    if request.user.is_authenticated:
        return redirect('frontend:dashboard', request.user.id)
    
    else:
        if request.method == 'POST':
            global first_name
            username = request.POST.get('email')
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            global email
            email = request.POST.get('email')
            password1 = request.POST.get('password')
            password2 = request.POST.get('password2')
            global token
            token =  str(random.randint(100001,999999))
    
            
            if User.objects.filter(email=email).exists():
                    messages.error(request, "User already exists.")
                    return redirect('signup')
    
            if not request.POST.get('password'):
                messages.error(request, "Password cannot be blank.")
                return redirect('signup')
    
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('signup')
    
            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "User already exists.")
                    return redirect('signup')
                else:
                    # global user
                    html_message = loader.render_to_string(
                    'templates/email.html',
                    {
                        'user_name': first_name,
                        'token':   token,
                      
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
                        [email],
                    )
                    mail.fail_silently = False
                    mail.content_subtype = 'html'
                    mail.send()
                    user = User.objects.create_user(username=username,last_name=last_name,first_name=first_name, password=password1, email=email)
                    
                    user.is_active = False
                    user.save()
                    return redirect('verifymail')
    
    
        return render(request, 'sign-up.html')



def signout(request):
    logout(request)
    return redirect('frontend:signup') 




def paymentLog(request, pk, transaction_id, status, amount ):
    user = User.objects.get(id=pk)
    current_date = date.today()
    allocation = 0
    if amount == 20:
        allocation = 200
    elif amount == 50:
        allocation = 1000
    elif amount == 100:
        allocation = 150000
    payment_log = PaymentLogs.objects.create(
            payer = user,
            amount = amount,
            transaction_id = transaction_id,
            status = status,
    )
    seller = Seller.objects.get(user=user)
    current_allocation = seller.receipt_allocation
    total_allocation = int(allocation) + int(current_allocation)
    seller = Seller.objects.filter(user=user).update(receipt_allocation = total_allocation)
    # seller.save()
    # seller.update(receipt_allocation = total_allocation)
    payment_log.save()

    return redirect ('frontend:dashboard', user.id)