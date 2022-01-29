from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from common.views import CommonContextMixin
from orders.forms import OrderForm
from baskets.models import Basket
from orders.models import Order, OrderItem


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
        self._create_order(form.data)
        return super(OrderCreateView, self).form_valid(form)

    def _create_order(self, data):
        billing_address = data.dict().pop('csrfmiddlewaretoken')
        order = Order.objects.create(user=self.request.user, billing_address=billing_address)
        order.create_order_items()
        return order
