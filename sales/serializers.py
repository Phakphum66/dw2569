from rest_framework import serializers
from .models import Order


class RecentOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_username = serializers.CharField(source='customer.username')
    product_name = serializers.CharField(source='product.name', default=None)
    product_sku = serializers.CharField(source='product.sku', default=None)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'customer_username',
            'product_name',
            'product_sku',
            'quantity',
            'total_price',
            'status',
            'transaction_status',
            'created_at',
        ]

    def get_customer_name(self, obj):
        full = obj.customer.get_full_name()
        return full if full else obj.customer.username
