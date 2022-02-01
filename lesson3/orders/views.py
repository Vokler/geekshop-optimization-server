from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.detail import DetailView

from common.views import CommonContextMixin
from orders.forms import OrderForm
from baskets.models import Basket
from orders.models import Order


class OrderCreateView(CommonContextMixin, FormView):
    title = 'GeekShop - Оформление заказа'
    form_class = OrderForm
    template_name = 'orders/checkout_order.html'
    success_url = reverse_lazy('orders:order_create')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

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
        message = 'Заказ №{} оформлен.' \
                  'Перейти к ' \
                  '<a href="{}" class="alert-link">списку заказов</a>'.format(obj.id, link)
        return message


class OrderListView(CommonContextMixin, ListView):
    title = 'GeekShop - Заказы'
    model = Order
    template_name = 'orders/orders.html'

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
