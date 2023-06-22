from django.contrib import admin
from django.urls import path
from . import views
from .views import Dashboard
from django.conf import settings
from django.conf.urls.static import static

app_name = "frontend"


urlpatterns = [
    path('', views.home, name="home"),
    path('documentation/', views.documentation, name='documentation'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/<int:pk>/', Dashboard.as_view(), name="dashboard"),
    

    
]

if settings.DEBUG == False:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)