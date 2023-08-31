from django.contrib import admin
from django.urls import path
from . import views
from .views import Dashboard, Home, SignUp
from django.conf import settings
from django.conf.urls.static import static




app_name = "frontend"


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('documentation/', views.documentation, name='documentation'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', views.signin, name='signin'),
    path('verifyemail/<int:pk>/', views.verifymail, name='verifymail'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    
]

if settings.DEBUG == False:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)