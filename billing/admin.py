from django.contrib import admin

from .models import BillingProfile, CreditCard, ChargeOrder

admin.site.register(BillingProfile)
admin.site.register(CreditCard)
admin.site.register(ChargeOrder)
