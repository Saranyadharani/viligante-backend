from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.scan_url, name='scan_url'),
]