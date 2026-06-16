from django.shortcuts import render
from .models import Product

def dashboard(request):
    products = Product.objects.all()
    total_products = products.count()
    total_value = sum(p.price * p.stock_quantity for p in products)
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_value': total_value,
    }
    return render(request, 'inventory/dashboard.html', context)
