from django.contrib import admin

from .models import GpaUser, BankAccount, Transaction

admin.site.register(GpaUser)
admin.site.register(BankAccount)
admin.site.register(Transaction)
