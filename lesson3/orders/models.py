from django.db import models

from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_address = models.JSONField(default=dict)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ №{self.id}'

    def create_order_items(self):
        baskets = self.user.basket_set.all()
        for basket in baskets:
            self.orderitem_set.create(product=basket.product, quantity=basket.quantity)
        baskets.delete()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=0)