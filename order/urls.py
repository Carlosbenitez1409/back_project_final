from django.urls import path
from .views import create_order, list_orders, order_detail

urlpatterns = [
    path('orders/', list_orders, name='list_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
]
