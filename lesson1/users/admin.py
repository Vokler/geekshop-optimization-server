from django.contrib import admin

from users.models import User, EmailVerification
from baskets.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    pass
