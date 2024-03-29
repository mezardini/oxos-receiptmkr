from django.shortcuts import render, redirect, get_object_or_404
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
        visitor_ip = visitor_ip = request.META.get('REMOTE_ADDR')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # The IP addresses are usually comma-separated.
            ip_list = x_forwarded_for.split(',')
            # The client's IP address is the first in the list.
            visitor_ip = ip_list[0].strip()
        else:
            # If 'HTTP_X_FORWARDED_FOR' is not present, use 'REMOTE_ADDR'.
            visitor_ip = request.META.get('REMOTE_ADDR')

        # current_datetime = datetime.now()
        current_datetime = datetime.today().strftime("%d %b, %y %H:%M:%S")
        send_mail(
            'New Visitor',
            'A visitor ' + visitor_ip + ' has been on Oxos-Receiptmkr at ' + current_datetime,
            'settings.EMAIL_HOST_USER',
            ['mezardini@gmail.com'],
            fail_silently=False,
        )
        # access_string = Home.string

        context = {}
        return render(request, 'index.html', context)

    def post(self, request):
        if request.method == 'POST':
            body = request.POST['message_body']
            sender = request.POST['sender_email']
            send_mail(
                'Message from ' + sender,
                body,
                'settings.EMAIL_HOST_USER',
                ['mezardini@gmail.com'],
                fail_silently=False,
            )


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

    def get(self, request):
        user = User.objects.get(id=request.user.id)

        if Seller.objects.filter(user=user).exists():
            biz = Seller.objects.get(user=user)
            receipts = ReceiptDetails.objects.filter(seller=biz)
            total_receipts = ReceiptRequest.objects.filter(
                user_no=biz.biz_code).count()

            specific_date = datetime(2023, 5, 29)
            current_date = datetime.now()
            days_difference = (specific_date - current_date).days
            receipts_allocated = biz.receipt_allocation
            receipts_allocated_text = receipts_allocated if receipts_allocated <= 100000 else 'Unlimited'

            bar_width_1 = 5 if total_receipts == 0 else (
                total_receipts / (total_receipts + receipts_allocated)) * 100
            bar_width_2 = (receipts_allocated /
                           (total_receipts + receipts_allocated)) * 100

            context = {
                'user': user,
                'biz': biz,
                'total_receipts': total_receipts,
                'days_difference': days_difference,
                'receipts_allocated': receipts_allocated_text,
                'bar_width_1': bar_width_1,
                'bar_width_2': bar_width_2,
                'receipts': receipts,
            }
            return render(request, self.template_name, context)

        else:
            biz_token = 'BC' + str(random.randint(11111, 99999)) + str(user.id)
            seller_biz = Seller.objects.create(
                user=user,
                biz_code=biz_token
            )
            seller_biz.save()
            return redirect('dashboard')


class SignUp(View):
    def generate_random_token(self):
        return str(random.randint(100001, 999999))

    def get(self, request):
        return render(request, 'sign-up.html')

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('email')
            first_name = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if User.objects.filter(email=email).exists():
                messages.error(request, "User already exists.")
                return redirect('frontend:signup')

            if not password1:
                messages.error(request, "Password cannot be blank.")
                return redirect('frontend:signup')

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('frontend:signup')

            token = self.generate_random_token()

            html_message = loader.render_to_string(
                'verify-email.html',
                {
                    'user': first_name,
                    'token': token
                }
            )

            send_mail(
                'Subject: Verify Your Account - Welcome to Oxos-ReceiptMkr!',
                html_message,
                'mezardini@gmail.com',
                [email],
                fail_silently=False,
            )

            user = User.objects.create_user(
                username=username, first_name=first_name, password=password1, email=email)
            user.is_active = False
            user.save()

            return redirect('frontend:verifymail', pk=user.id)

        return render(request, 'sign-up.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        if not request.POST.get('email'):
            messages.error(request, "Email cannot be blank.")
            return redirect('frontend:signin')

        if not request.POST.get('password'):
            messages.error(request, "Password cannot be blank.")
            return redirect('frontend:signin')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('frontend:dashboard')
        else:
            messages.error(request, "Incorrect username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def verifymail(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        entered_token = request.POST.get('token')

        if entered_token == SignUp.token:
            user.is_active = True
            user.save()
            messages.success(request, "Email validated. You can now sign in.")
            return redirect('frontend:signin')

        messages.error(request, "Token incorrect.")
        user.is_active = False
        user.save()
        return redirect('frontend:verifymail')

    return render(request, 'verify.html')


def signout(request):
    logout(request)
    return redirect('frontend:signin')
