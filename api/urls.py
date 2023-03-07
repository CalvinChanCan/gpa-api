from django.urls import path, include  # Ensure `include` is imported
from rest_framework import routers
from gpa.views import (
    UserViewSet,
    TransactionViewSet,
    AccountViewSet,
    UserTransactionViewSet,
    AccountTransactionViewSet,
    SignInView,
    SignUpView,
)

router = routers.DefaultRouter()

router.register(
    r"users",
    UserViewSet,
    basename="user",
)
router.register(
    r"transactions",
    TransactionViewSet,
    basename="transactions",
)

router.register(
    r"accounts",
    AccountViewSet,
    basename="accounts",
)

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signup/", SignUpView.as_view(), name="sign-up"),
    path(
        "api/users/<int:user_id>/accounts/",
        AccountViewSet.as_view({"get": "list"}),
        name="user-accounts",
    ),
    path(
        "api/accounts/<int:account_id>/balance/<str:date>/",
        AccountViewSet.as_view({"get": "balance"}),
        name="account-balance",
    ),
    path(
        "api/users/<int:user_id>/accounts/create/",
        AccountViewSet.as_view({"post": "post"}),
        name="create-account",
    ),
    path(
        "api/users/<int:user_id>/transactions/",
        UserTransactionViewSet.as_view({"get": "list"}),
        name="user-transactions",
    ),
    path(
        "api/accounts/<int:account_id>/transactions/",
        AccountTransactionViewSet.as_view({"get": "list"}),
        name="account-transactions",
    ),
    path(
        "api/accounts/<int:account_id>/transactions/create/",
        TransactionViewSet.as_view({"post": "post"}),
        name="create-transaction",
    ),
]
