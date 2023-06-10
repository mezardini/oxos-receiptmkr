from django.shortcuts import render, redirect
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

# Create your views here.




def home(request):
    

    return render(request, 'index.html')

def documentation(request):
    

    return render(request, 'api-doc.html')

def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')
@login_required(login_url='frontend:signup')
def dashboard(request, pk):
    
    user = User.objects.get(id=pk)
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
                   'days_difference':days_difference, 'receipts_allocated':receipts_allocated, 'bar_width_1':bar_width_1, 'bar_width_2':bar_width_2  }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('frontend:home')




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



@login_required(login_url='frontend:signup')
def payment(request, pk):
    user = User.objects.get(id=pk)
    base_5 = 'Basic'
    base_10 = 'Medium'
    base_25 = 'Large'
    current_date = date.today()
    allocation = 20

    if request.method == 'POST':
        if request.POST['template_choice'] == '5':
            allocation = 50
            user_group = Group.objects.get(name=base_5)
            user.groups.add(user_group)
            return redirect('https://business.quickteller.com/link/pay/oxos')
        elif request.POST['template_choice'] == '10':
            allocation = 200
            user_group = Group.objects.get(name=base_10)
            user.groups.add(user_group)
            return redirect('https://business.quickteller.com/link/pay/tixvanaUKxsv')
        elif request.POST['template_choice'] == '25':
            allocation = 500
            user_group = Group.objects.get(name=base_25)
            user.groups.add(user_group)
        # return redirect('https://business.quickteller.com/link/pay/tixvanaUKxsv')
        payment_log = PaymentLogs.objects.create(
            payer = user,
            amount = request.POST['template_choice'],
            transaction_id = request.POST['template_choice'],
            status = request.POST['template_choice'],
            expiration_date = current_date + timedelta(days=30),
        )
        seller = Seller.objects.get(user=user)
        current_allocation = seller.receipt_allocation
        total_allocation = int(allocation) + int(current_allocation)
        seller.update(receipt_allocation = total_allocation)
        payment_log.save()

    context = {'user':user}
    return render(request, 'pay.html', context)



# def paymentLog(request):
#     current_date = date.today()
#     payment_log = PaymentLogs.objects.create(
#             payer = user,
#             amount = request.POST['template_choice'],
#             transaction_id = request.POST['template_choice'],
#             status = request.POST['template_choice'],
#             expiration_date = current_date + timedelta(days=30),
#     )
#     seller = Seller.objects.get(user=user)
#     current_allocation = seller.receipt_allocation
#     total_allocation = int(allocation) + int(current_allocation)
#     seller.update(receipt_allocation = total_allocation)
#     payment_log.save()