from django.urls import path
from . import views

urlpatterns = [
    path('', views.scan_url, name='scan_url'),  # Change this line
]
