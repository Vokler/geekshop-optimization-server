from django.views.generic.edit import CreateView

from orders.models import Order
from users.forms import UserProfileForm


class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/checkout_order.html'
    form_class = UserProfileForm
