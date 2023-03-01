from django.urls import path, include  # Ensure `include` is imported
from rest_framework import routers
from gpa.views import UserViewSet, TransactionViewSet, BankAccountViewSet

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
router.register(r"accounts", BankAccountViewSet, basename="accounts")


from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/accounts/<int:pk>/balance/",
        BankAccountViewSet.as_view({"get": "account_balance"}),
    ),
]
