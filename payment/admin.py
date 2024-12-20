from django.contrib import admin

from .models import PaymentProfile, Transaction

admin.site.register(PaymentProfile)
admin.site.register(Transaction)