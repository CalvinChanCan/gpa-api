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

    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        transactions = Transaction.objects.filter(account_id=pk)
        balance = 0
        for transaction in transactions:
            if transaction.transaction_type == "CREDIT":
                balance += transaction.amount
            elif transaction.transaction_type == "DEBIT":
                balance -= transaction.amount
        return Response({"balance": balance})
