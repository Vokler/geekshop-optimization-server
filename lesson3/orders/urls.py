from django.urls import path

from orders.views import OrderCreateView, OrderListView


app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='order_list'),
]
