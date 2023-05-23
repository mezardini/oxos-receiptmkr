from django.contrib import admin
from django.urls import path
from . import views

app_name = "frontend"


urlpatterns = [
    path('', views.home, name="home"),
    path('documentation/', views.documentation, name='documentation'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.login, name='signin'),
    path('verifymail/', views.verifymail, name='verifymail'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/<int:pk>/', views.dashboard, name="dashboard"),
    path('payment/<int:pk>/', views.payment, name="payment"),
    path('payment/<int:pk>/', views.payment, name="payment"),
    path('create_biz/', views.registerBusiness, name='regBiz'),
    path('cart/', views.cart, name='cart'),
]