from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from inventory.models import Product, Category
from .models import Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    cart = get_cart(request)

    context = {
        "categories": categories,
        "products": products,
        "cart_items_count": cart.total_items,
        "search_query": query,
    }
    return render(request, 'web_sales/home.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('web_sales:home')

def view_cart(request):
    cart = get_cart(request)
    context = {
        "cart": cart,
        "cart_items_count": cart.total_items,
    }
    return render(request, 'web_sales/cart.html', context)
