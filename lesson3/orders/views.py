from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from common.views import CommonContextMixin
from orders.forms import OrderForm
from orders.models import Order


class OrderCreateView(CommonContextMixin, FormView):
    title = 'GeekShop - Оформление заказа'
    form_class = OrderForm
    template_name = 'orders/checkout_order.html'
    success_url = reverse_lazy('orders:order_create')

    def form_valid(self, form):
        order = self._create_order(form.data)
        messages.success(self.request, self._create_success_message(order))
        return super(OrderCreateView, self).form_valid(form)

    def _create_order(self, data):
        billing_address = data.dict()
        billing_address.pop('csrfmiddlewaretoken')
        order = Order.objects.create(user=self.request.user, billing_address=billing_address)
        order.create_order_items()
        return order

    def _create_success_message(self, obj):
        link = reverse('orders:order_list')
        message = 'Заказ №{} оформлен. ' \
                  'Перейти к ' \
                  '<a href="{}" class="alert-link">списку заказов</a>'.format(obj.id, link)
        return mark_safe(message)


class OrderListView(CommonContextMixin, ListView):
    title = 'GeekShop - Заказы'
    model = Order
    template_name = 'orders/orders.html'
    ordering = ('-created_timestamp',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class OrderDetailView(CommonContextMixin, DetailView):
    model = Order
    template_name = 'orders/order.html'

    def get_title(self):
        return f'GeekShop - Заказ №{self.object.id}'

    def get_queryset(self):
        queryset = super(OrderDetailView, self).get_queryset()
        return queryset.filter(user=self.request.user)
