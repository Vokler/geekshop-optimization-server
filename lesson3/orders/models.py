from django.db import models

from users.models import User
from products.models import Product


class Order(models.Model):
    BEING_PROCESSED = 'being_processed'
    ON_THE_WAY = 'on_the_way'
    DELIVERED = 'delivered'

    STATUSES = (
        (BEING_PROCESSED, 'Оформляется'),
        (ON_THE_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_address = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUSES, default=BEING_PROCESSED)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ №{self.id}'

    def total_sum(self):
        return sum(item.sum() for item in self.orderitem_set.all())

    def create_order_items(self):
        baskets = self.user.basket_set.all()
        for basket in baskets:
            self.orderitem_set.create(product=basket.product, quantity=basket.quantity)
        baskets.delete()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=0)

    def sum(self):
        return self.product.price * self.quantity
