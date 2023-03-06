from rest_framework import serializers
from .models import GpaUser, Transaction, BankAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpaUser
        fields = "__all__"


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ("account_id","id")


class TransactionSerializer(serializers.ModelSerializer):
    account = BankAccountSerializer(read_only=True, source="account_id")

    class Meta:
        model = Transaction
        fields = (
            "id",
            "transaction_date",
            "amount",
            "notes",
            "transaction_type",
            "account",
        )
