import os
import random
import time
from datetime import timedelta
from decimal import Decimal

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from inventory.models import Product
from sales.models import Order

User = get_user_model()

TOTAL_RECORDS = 2_000_000
BATCH_SIZE = 5000
COMPLETED_RATIO = 0.8

TRANSACTION_STATUSES = ['completed', 'pending', 'failed', 'refunded']
TRANSACTION_WEIGHTS = [COMPLETED_RATIO, 0.1, 0.05, 0.05]

ORDER_STATUSES = ['pending', 'completed', 'cancelled']
ORDER_WEIGHTS = [0.1, 0.85, 0.05]


def main():
    users = list(User.objects.all())
    products = list(Product.objects.all())

    if not users:
        print("No users found. Create at least one user first.")
        return
    if not products:
        print("No products found. Create at least one product first.")
        return

    start_time = time.time()
    print(f"Generating {TOTAL_RECORDS:,} sale records...")
    print(f"Users: {len(users)}, Products: {len(products)}")
    print(f"Batch size: {BATCH_SIZE:,}")

    order_objects = []
    total_created = 0
    batch_start = 1

    for i in range(1, TOTAL_RECORDS + 1):
        customer = random.choice(users)
        product = random.choice(products)
        quantity = random.randint(1, 10)
        discount_mult = Decimal(1) - Decimal(product.discount_percent) / Decimal(100)
        total_price = (product.price * quantity * discount_mult).quantize(Decimal('0.01'))
        transaction_status = random.choices(TRANSACTION_STATUSES, weights=TRANSACTION_WEIGHTS, k=1)[0]
        order_status = random.choices(ORDER_STATUSES, weights=ORDER_WEIGHTS, k=1)[0]
        days_ago = random.randint(0, 365)
        created_at = timezone.now() - timedelta(days=days_ago)

        order_objects.append(Order(
            order_number=f"ORD-{timezone.now():%Y%m%d}-{i:07d}",
            customer=customer,
            product=product,
            quantity=quantity,
            total_price=total_price,
            status=order_status,
            transaction_status=transaction_status,
            created_at=created_at,
            updated_at=created_at,
        ))

        if len(order_objects) == BATCH_SIZE:
            with transaction.atomic():
                Order.objects.bulk_create(order_objects)
            total_created += len(order_objects)
            elapsed = time.time() - start_time
            rate = total_created / elapsed if elapsed > 0 else 0
            print(f"  Created {total_created:>10,} / {TOTAL_RECORDS:,} records ({rate:,.0f} records/sec)")
            order_objects = []

    if order_objects:
        with transaction.atomic():
            Order.objects.bulk_create(order_objects)
        total_created += len(order_objects)

    elapsed = time.time() - start_time
    print(f"\nDone! Created {total_created:,} orders in {elapsed:.2f} seconds.")
    print(f"Average speed: {total_created / elapsed:,.0f} records/sec")


if __name__ == '__main__':
    main()
