from django.urls import path
from . import views

app_name = 'web_sales'

urlpatterns = [
    path('', views.home, name='home'),
]
