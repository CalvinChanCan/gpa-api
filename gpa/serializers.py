from rest_framework import serializers
from .models import GpaUser, Transaction, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpaUser
        fields = ["id", "email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = GpaUser(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("account_id", "id")


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
