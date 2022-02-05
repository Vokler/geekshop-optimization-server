from django.contrib import admin

from baskets.admin import BasketAdmin
from users.models import EmailVerification, User, UserLocation


class UserLocationAdminInline(admin.TabularInline):
    model = UserLocation
    fields = ('city', 'country')
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdmin, UserLocationAdminInline)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
