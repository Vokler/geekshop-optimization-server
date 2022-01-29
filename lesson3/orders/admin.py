from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    fields = ('id', 'product', 'quantity')
    readonly_fields = ('product', 'quantity')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'created_timestamp')
    fields = ('user', 'billing_address', ('created_timestamp', 'updated_timestamp'))
    readonly_fields = ('created_timestamp', 'updated_timestamp')
    inlines = (OrderItemAdminInline,)
