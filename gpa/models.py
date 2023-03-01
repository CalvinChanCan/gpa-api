from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator


class User(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=100, validators=[EmailValidator()])
    password_hash = models.CharField(max_length=128, null=False, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(
        max_length=16, unique=True, blank=False, validators=[MinLengthValidator(16)]
    )


class Transaction(models.Model):
    account_id = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(null=False, blank=False)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        validators=[MinValueValidator(0.01)],
    )
    notes = models.TextField(null=True)
    transaction_type = models.CharField(
        max_length=6,
        choices=[
            ("CREDIT", "Credit"),
            ("DEBIT", "Debit"),
        ],
    )
