from datetime import timedelta

from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import RecentOrderSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overview(request):
    try:
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        stats = Order.objects.aggregate(
            total_revenue=Sum('total_price'),
            total_orders=Count('id'),
            avg_order_value=Avg('total_price'),
            completed_orders=Count('id', filter=Q(status='completed')),
            cancelled_orders=Count('id', filter=Q(status='cancelled')),
            pending_orders=Count('id', filter=Q(status='pending')),
            today_revenue=Sum('total_price', filter=Q(created_at__gte=today_start)),
            today_orders=Count('id', filter=Q(created_at__gte=today_start)),
        )

        data = {
            'total_revenue': float(stats['total_revenue'] or 0),
            'total_orders': stats['total_orders'],
            'average_order_value': round(float(stats['avg_order_value'] or 0), 2),
            'completed_orders': stats['completed_orders'],
            'cancelled_orders': stats['cancelled_orders'],
            'pending_orders': stats['pending_orders'],
            'today_revenue': float(stats['today_revenue'] or 0),
            'today_orders': stats['today_orders'],
        }
        return Response(data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch overview statistics', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def revenue_trend(request):
    try:
        days = request.GET.get('days', 30)
        try:
            days = int(days)
        except (ValueError, TypeError):
            days = 30
        days = max(1, min(365, days))

        now = timezone.now()
        since = now - timedelta(days=days)

        trend = (
            Order.objects
            .filter(created_at__gte=since)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(
                revenue=Sum('total_price'),
                order_count=Count('id'),
            )
            .order_by('date')
        )

        results = [
            {
                'date': entry['date'],
                'revenue': float(entry['revenue'] or 0),
                'order_count': entry['order_count'],
            }
            for entry in trend
        ]

        return Response({
            'days': days,
            'data': results,
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch revenue trend', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_products(request):
    try:
        limit = request.GET.get('limit', 10)
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 10
        limit = max(1, min(100, limit))

        days = request.GET.get('days', None)
        qs = Order.objects.filter(product__isnull=False)
        if days:
            try:
                days = int(days)
                since = timezone.now() - timedelta(days=days)
                qs = qs.filter(created_at__gte=since)
            except (ValueError, TypeError):
                pass

        products = (
            qs
            .values('product__id', 'product__name', 'product__category__name')
            .annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('total_price'),
                order_count=Count('id'),
            )
            .order_by('-total_revenue')[:limit]
        )

        results = [
            {
                'product_id': p['product__id'],
                'product_name': p['product__name'],
                'category_name': p['product__category__name'],
                'total_quantity': p['total_quantity'],
                'total_revenue': float(p['total_revenue'] or 0),
                'order_count': p['order_count'],
            }
            for p in products
        ]

        return Response({
            'limit': limit,
            'data': results,
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch top products', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def status_distribution(request):
    try:
        status_counts = (
            Order.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )

        transaction_counts = (
            Order.objects
            .values('transaction_status')
            .annotate(count=Count('id'))
            .order_by('transaction_status')
        )

        total = Order.objects.count()

        data = {
            'total_orders': total,
            'by_order_status': {
                entry['status']: entry['count']
                for entry in status_counts
            },
            'by_transaction_status': {
                entry['transaction_status']: entry['count']
                for entry in transaction_counts
            },
        }
        return Response(data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch status distribution', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_orders(request):
    try:
        limit = request.GET.get('limit', 20)
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 20
        limit = max(1, min(200, limit))

        orders = (
            Order.objects
            .select_related('product', 'customer')
            .order_by('-created_at')[:limit]
        )

        serializer = RecentOrderSerializer(orders, many=True)
        return Response({
            'limit': limit,
            'data': serializer.data,
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch recent orders', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
