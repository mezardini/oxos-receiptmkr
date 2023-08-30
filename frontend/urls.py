from django.contrib import admin
from django.urls import path
from . import views
from .views import Dashboard, Home
from django.conf import settings
from django.conf.urls.static import static

app_name = "frontend"


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('documentation/', views.documentation, name='documentation'),
    path('signup/', views.signup, name='signup'),
    
    path('signout/', views.signout, name='signout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    # path('payment/<int:pk>/<str:transaction_id>/<str:status>/<int:amount>/', views.paymentLog, name='paymentlog'),

    
]

if settings.DEBUG == False:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)