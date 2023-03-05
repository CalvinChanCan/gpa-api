from rest_framework import serializers
from .models import GpaUser, Transaction, BankAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpaUser
        fields = "__all__"


class BankAccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BankAccount
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
