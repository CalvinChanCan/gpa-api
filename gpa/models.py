from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator, MinValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class GpaUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=100, validators=[EmailValidator()], unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    groups = models.ManyToManyField(
        Group,
        related_name="gpa_users",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_query_name="gpa_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="gpa_users",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="gpa_user",
    )

    def __str__(self):
        return self.email


class BankAccount(models.Model):
    user = models.ForeignKey(GpaUser, on_delete=models.CASCADE)
    account_num = models.CharField(
        max_length=16, unique=True, blank=False, validators=[MinLengthValidator(16)]
    )


class Transaction(models.Model):
    account_id = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(null=False, blank=False)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        validators=[MinValueValidator(0.01)],
    )
    notes = models.TextField(null=True)
    transaction_type = models.CharField(
        max_length=6,
        choices=[
            ("CREDIT", "Credit"),
            ("DEBIT", "Debit"),
        ],
    )
