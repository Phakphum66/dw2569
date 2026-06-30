from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from inventory.models import Product, Category
from sales.models import Order
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


def _generate_order_number():
    now = timezone.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    import random
    suffix = ''.join(random.choices('0123456789ABCDEF', k=6))
    return f"ORD-{timestamp}-{suffix}"


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
        "cart_total": cart.total_price,
    }
    return render(request, 'web_sales/cart.html', context)


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, 'ตะกร้าสินค้าของคุณว่างเปล่า')
        return redirect('web_sales:view_cart')

    cart_items = cart.items.select_related('product').all()
    errors = []
    valid_items = []

    for item in cart_items:
        product = item.product
        if not product:
            errors.append(f"สินค้าถูกลบออกจากระบบแล้ว: {item.product_id}")
            continue
        if product.stock_quantity < item.quantity:
            errors.append(
                f"สินค้า '{product.name}' มี stock ไม่เพียงพอ "
                f"(ต้องการ {item.quantity}, มี {product.stock_quantity})"
            )
            continue
        valid_items.append(item)

    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('web_sales:view_cart')

    created_orders = []
    try:
        with db_transaction.atomic():
            for item in valid_items:
                product = item.product
                order_number = _generate_order_number()
                discount_mult = Decimal(1) - Decimal(product.discount_percent) / Decimal(100)
                unit_price = product.price * discount_mult
                total_price = (unit_price * item.quantity).quantize(Decimal('0.01'))

                order = Order.objects.create(
                    order_number=order_number,
                    customer=request.user,
                    product=product,
                    quantity=item.quantity,
                    total_price=total_price,
                    status=Order.StatusChoices.PENDING,
                    transaction_status=Order.TransactionStatusChoices.PENDING,
                )
                created_orders.append(order)

                Product.objects.filter(id=product.id).update(
                    stock_quantity=product.stock_quantity - item.quantity,
                    sales_count=product.sales_count + item.quantity,
                )

            cart.items.all().delete()

        messages.success(
            request,
            f'ชำระเงินสำเร็จ! สร้างคำสั่งซื้อ {len(created_orders)} รายการ '
            f'รวม {sum(float(o.total_price) for o in created_orders):,.2f} บาท'
        )
        return render(request, 'web_sales/checkout_success.html', {
            'orders': created_orders,
            'total_amount': sum(o.total_price for o in created_orders),
        })

    except Exception as e:
        messages.error(request, f'เกิดข้อผิดพลาดในการชำระเงิน: {str(e)}')
        return redirect('web_sales:view_cart')
