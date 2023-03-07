from django.contrib import admin

from .models import GpaUser, Account, Transaction

admin.site.register(GpaUser)
admin.site.register(Account)
admin.site.register(Transaction)
