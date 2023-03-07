from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GpaUser, Transaction, Account
from .serializers import UserSerializer, TransactionSerializer, AccountSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "success": "User created successfully",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


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
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(
            {"success": "User signed in successfully", "user": user_data},
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = GpaUser.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def post(self, request, **kwargs):
        account_id = kwargs.get("account_id")
        account = Account.objects.get(id=account_id)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            transaction_type = serializer.validated_data["transaction_type"]
            transaction_date = serializer.validated_data["transaction_date"]
            print(transaction_date)

            transaction = Transaction.objects.create(
                account_id=account,
                amount=amount,
                transaction_type=transaction_type,
                transaction_date=transaction_date,
            )

            # Update account balance
            if transaction_type == "CREDIT":
                account.balance += amount
            elif transaction_type == "DEBIT":
                account.balance -= amount
            account.save()

            return Response(
                {
                    "success": "Transaction created successfully",
                    "transaction": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        queryset = Account.objects.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
