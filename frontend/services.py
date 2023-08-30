# from frontend.models import Seller, PaymentLogs, ReceiptDetails
# from django.contrib.auth.models import User, auth, Group
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# import random




# def create_seller_account(request, id):
#     user = User.objects.get(id=id)
#     biz_token = 'BC'+ str(random.randint(11111,99999)) + str(user.id)
    

#     users_in_group = Group.objects.get(name="Business").user_set.all()
#     if user not in users_in_group :
#         seller_biz = Seller.objects.create(
#             user = user,
#             biz_code = biz_token
#         )
#         seller_biz.save()
#         user_group = Group.objects.get(name="Business")
#         user.groups.add(user_group)
        
#         return redirect('frontend:dashboard')
    # return render(request, 'dashboard.html')

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from frontend.models import Seller  # Import the Seller model from your app
import random

def create_seller_account(request, id):  # Note that 'request' should be added as the first parameter
    user = User.objects.get(id=id)
    biz_token = 'BC'+ str(random.randint(11111,99999)) + str(user.id)
    
    # users_in_group = Group.objects.get(name="Business").user_set.all()
    # if user not in users_in_group:
    seller_biz = Seller.objects.create(
        user=user,
        biz_code=biz_token
    )
    seller_biz.save()
        # user_group = Group.objects.get(name="Business")
        # user.groups.add(user_group)
    return redirect('frontend:dashboard') 
    # return redirect('frontend:dashboard')

            