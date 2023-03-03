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

router.register(
    r"accounts",
    BankAccountViewSet,
    basename="accounts",
)


from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/users/<int:user_id>/accounts/",
        BankAccountViewSet.as_view({"get": "list"}),
        name="user-accounts",
    ),
]
