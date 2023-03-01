from django.db import models


class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    password_hash = models.TextField()
    email = models.TextField()


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.TextField()


class Transaction(models.Model):
    account_number = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField()
