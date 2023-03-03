from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Transaction, BankAccount
from .serializers import UserSerializer, TransactionSerializer, BankAccountSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        queryset = BankAccount.objects.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)

        # Add balance to each account
        for account in serializer.data:
            transactions = Transaction.objects.filter(account_id=account["id"])
            balance = 0
            for transaction in transactions:
                if transaction.transaction_type == "CREDIT":
                    balance += transaction.amount
                elif transaction.transaction_type == "DEBIT":
                    balance -= transaction.amount
            account["balance"] = balance

        return Response(serializer.data)
