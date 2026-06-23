import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction as db_transaction

from accounts.models import User
from inventory.models import Product
from sales.models import Order


class Command(BaseCommand):
    help = 'Generate 100,000 sale records with 80% completed transactions'

    BATCH_SIZE = 1000
    TOTAL_RECORDS = 100_000

    def handle(self, *args, **options):
        users = list(User.objects.all())
        products = list(Product.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Create users first.'))
            return
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Run seed_products first.'))
            return

        self.stdout.write(f'Generating {self.TOTAL_RECORDS} orders...')
        self.stdout.write(f'Users: {len(users)}, Products: {len(products)}')

        Order.objects.all().delete()

        orders = []
        total_batches = self.TOTAL_RECORDS // self.BATCH_SIZE

        for batch_num in range(total_batches):
            for _ in range(self.BATCH_SIZE):
                is_completed = random.random() < 0.8
                customer = random.choice(users)
                product = random.choice(products)
                quantity = random.randint(1, 5)
                unit_price = float(product.price) * (1 - product.discount_percent / 100)
                total_price = round(unit_price * quantity, 2)
                days_ago = random.randint(0, 365)
                created_at = timezone.now() - timedelta(days=days_ago)

                if is_completed:
                    status = Order.StatusChoices.COMPLETED
                    txn_status = Order.TransactionStatusChoices.COMPLETED
                else:
                    status = random.choice([
                        Order.StatusChoices.PENDING,
                        Order.StatusChoices.CANCELLED,
                    ])
                    txn_status = random.choice([
                        Order.TransactionStatusChoices.PENDING,
                        Order.TransactionStatusChoices.FAILED,
                        Order.TransactionStatusChoices.REFUNDED,
                    ])

                order = Order(
                    order_number=f'ORD-{created_at.strftime("%Y%m%d")}-{batch_num * self.BATCH_SIZE + len(orders) + 1:06d}',
                    customer=customer,
                    product=product,
                    quantity=quantity,
                    total_price=total_price,
                    status=status,
                    transaction_status=txn_status,
                    created_at=created_at,
                )
                orders.append(order)

            with db_transaction.atomic():
                Order.objects.bulk_create(orders, ignore_conflicts=True)

            self.stdout.write(
                f'  Batch {batch_num + 1}/{total_batches} completed '
                f'({(batch_num + 1) * self.BATCH_SIZE} records)'
            )
            orders.clear()

        completed_count = Order.objects.filter(transaction_status='completed').count()
        self.stdout.write(self.style.SUCCESS(
            f'Done. Total orders: {Order.objects.count()}, '
            f'Completed transactions: {completed_count} '
            f'({completed_count / self.TOTAL_RECORDS * 100:.1f}%)'
        ))
