from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GpaUser, Transaction, BankAccount
from .serializers import UserSerializer, TransactionSerializer, BankAccountSerializer


class SignInView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND
            )
        login(request, user)
        return Response(
            {"success": "User signed in successfully"}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = GpaUser.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class UserTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Transaction.objects.filter(account_id__user_id=user_id)


class AccountTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        account_id = self.kwargs.get("account_id")
        return Transaction.objects.filter(account_id=account_id)


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
