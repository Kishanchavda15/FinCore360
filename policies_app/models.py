from django.db import models
from django.core.exceptions import ValidationError

from accounts_app.models import User
from clients_app.models import ClientProfile
from products_app.models import Product, ProductType


class Policy(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("completed", "Completed"),
    )

    INSTALLMENT_CHOICES = (
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("half_yearly", "Half-Yearly"),
        ("yearly", "Yearly"),
    )

    name = models.CharField(max_length=255)

    # Changed to ForeignKey – now dynamic!
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,  # Prevent deletion if used in policies
        related_name="policies"
    )
    product_subtype = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="policies"
    )

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="client_policies")
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="staff_managed_policies")

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    installment_frequency = models.CharField(max_length=20, choices=INSTALLMENT_CHOICES, default="monthly")
    duration_time = models.PositiveIntegerField(null=True, blank=True)
    start_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate that the subtype belongs to the selected type
        if self.product_type and self.product_subtype:
            if self.product_subtype.product_type != self.product_type:
                raise ValidationError({
                    "product_subtype": "This product subtype does not belong to the selected product type."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.product_type.name}"