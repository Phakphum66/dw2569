from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('dashboard/overview/', views.overview, name='dashboard-overview'),
    path('dashboard/revenue-trend/', views.revenue_trend, name='dashboard-revenue-trend'),
    path('dashboard/top-products/', views.top_products, name='dashboard-top-products'),
    path('dashboard/status-distribution/', views.status_distribution, name='dashboard-status-distribution'),
    path('dashboard/recent-orders/', views.recent_orders, name='dashboard-recent-orders'),
]
