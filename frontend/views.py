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
from datetime import datetime
from django.conf import settings
from core_api.models import Business
from core_api.models import ReceiptRequest

# Create your views here.




def home(request):
    

    return render(request, 'index.html')

def documentation(request):
    

    return render(request, 'api-doc.html')

def cart(request):
    # name = str(request.POST.get('name'))
    # product = str(request.POST.get('product'))
    # price = str(request.POST.get('price'))
    # biz_code = str(request.POST.get('biz_id'))
        
    # Response = requests.post('http://127.0.0.1:8000/api/getpdf/'+biz_code+'/'+name+'/'+product+'/'+price+'/').content
    # return HttpResponse(Response,content_type='application/pdf')
    if request.method == 'POST':
        name = str(request.POST.get('name'))
        product = str(request.POST.get('product'))
        price = str(request.POST.get('price'))
        biz_code = str(request.POST.get('biz_id'))

        response = requests.post('http://127.0.0.1:8000/api/getpdf/'+biz_code+'/'+name+'/'+product+'/'+price+'/').content
        # response['Content-Disposition'] = 'attachment; file=response'
        
        response =  HttpResponse(response,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+name+'.pdf'

        return response

    return render(request, 'home.html')
@login_required(login_url='signup')
def dashboard(request, pk):
    user = User.objects.get(id=pk)
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

    group_names = ['Lev 1', 'Group 2', 'Group 3']
    user_plan_and_text = {'Level 1':'You are on basic plan, your plan expires on 20th June, 2023', 'Level 2':'You are on medium plan, your plan expires on 20th June, 2023', 'Level 3':'You are on Enterprise plan, your plan expires on 20th June, 2023' }
    subscription_text = 'You are on free trial, your plan expires on 20th June, 2023'
    users_in_group = Group.objects.get(name="Business").user_set.all()
    users_in_group3 = Group.objects.get(name="Level 3").user_set.all()
    users_in_group2 = Group.objects.get(name="Level 2").user_set.all()
    if user in users_in_group:
        subscription_text = user_plan_and_text['Level 1']
    
    elif user in users_in_group2:
        subscription_text = user_plan_and_text['Level 2']
    
    elif user in users_in_group3:
        subscription_text = user_plan_and_text['Level 3']


    context = {'user':user, 'biz':biz, 'text':subscription_text, 'total_receipts':total_receipts, 'days_difference':days_difference}
    return render(request, 'dashboard.html', context)

def payment(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST.get('price') == '5':
            user_group = Group.objects.get(name="Level 1")
            user.groups.add(user_group)
        elif request.POST.get('price')  == '10':
            user_group = Group.objects.get(name="Level 2")
            user.groups.add(user_group)
        elif request.POST.get('price')  == '20':
            user_group = Group.objects.get(name="Level 3")
            user.groups.add(user_group)
    return render(request, 'payment.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']

        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard', pk=user.id)
        else:
            return render(request, 'log-in.html')
    context = {}
    return render(request, 'log-in.html', context)

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

def verifymail(request):

    if request.method == 'POST':
        
        entetoken = request.POST.get('token')
        entered_token = str(entetoken)

        if entered_token == token:
            messages.error(request, "Email validated, you can now signin.")
            user.is_active = True
            user.save()
            return redirect('signin')

        else:
            messages.error(request, "Token incorrect.")
            user.is_active = False
            user.save()
            return redirect('signup')


    return render(request, 'verifymail.html')

def signout(request):
    logout(request)
    return redirect('frontend:signup') 

def registerBusiness(request):
        user = request.user
        users_in_group = Group.objects.get(name="Business").user_set.all()
        if user in users_in_group :
            return redirect ('frontend:dashboard', user.id)
        else:
            biz_name = str(request.POST.get('name'))
            biz_website = str(request.POST.get('web_url'))
            biz_code = str(random.randint(1000,123999999))

            Response = requests.post('http://127.0.0.1:8000/api/createBiz/'+biz_name+'/'+biz_website+'/'+biz_code+'/')
            if request.method == 'POST':
                biz = Seller.objects.create(
                    biz_name = request.POST['name'],
                    biz_code = biz_code,
                    web_url = request.POST['web_url'],
                    user = User.objects.get(id=1)
                )
                biz.save()
                user_group = Group.objects.get(name="Business")
                user.groups.add(user_group)
                return redirect('/')
            return render(request, 'createbiz.html')
        # Output = response
        # data = json.loads(response.content)

        # url = 'https://127.0.0.1:8000/verify'   
        # page = requests.get(url, verify=False)

        # x = data.get("data").get("account_name")
        
        # return HttpResponse(Response)

@login_required(login_url='login')
def payment(request, pk):
    user = User.objects.get(id=pk)
    base_5 = 'Level 1'
    base_10 = 'Level 2'
    base_25 = 'Level 2'

    if request.method == 'POST':
        if request.POST['template_choice'] == '5':
            user_group = Group.objects.get(name=base_5)
            user.groups.add(user_group)
            return redirect('https://business.quickteller.com/link/pay/oxos')
        elif request.POST['template_choice'] == '10':
            user_group = Group.objects.get(name=base_10)
            user.groups.add(user_group)
            return redirect('https://business.quickteller.com/link/pay/tixvanaUKxsv')
        elif request.POST['template_choice'] == '25':
            user_group = Group.objects.get(name=base_25)
            user.groups.add(user_group)
        # return redirect('https://business.quickteller.com/link/pay/tixvanaUKxsv')

    context = {'user':user}
    return render(request, 'pay.html', context)