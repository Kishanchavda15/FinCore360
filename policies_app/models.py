from django.db import models
from django.core.exceptions import ValidationError

from accounts_app.models import User
from clients_app.models import ClientProfile


class Policy(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ("loan", "Loan"),
        ("insurance", "Insurance"),
        ("finance", "Finance"),
    )

    PRODUCT_SUBTYPE_CHOICES = (
        ("home_loan", "Home Loan"),
        ("gold_loan", "Gold Loan"),
        ("personal_loan", "Personal Loan"),
        ("education_loan", "Education Loan"),

        ("health_insurance", "Health Insurance"),
        ("vehicle_insurance", "Vehicle Insurance"),
        ("life_insurance", "Life Insurance"),
        ("travel_insurance", "Travel Insurance"),

        ("consumer_finance", "Consumer Finance"),
        ("business_finance", "Business Finance"),
        ("asset_finance", "Asset Finance"),
        ("project_finance", "Project Finance"),
    )

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

    # Clean mapping (class-level constant, not recreated every save)
    PRODUCT_MAPPING = {
        "loan": [
            "home_loan",
            "gold_loan",
            "personal_loan",
            "education_loan",
        ],
        "insurance": [
            "health_insurance",
            "vehicle_insurance",
            "life_insurance",
            "travel_insurance",
        ],
        "finance": [
            "consumer_finance",
            "business_finance",
            "asset_finance",
            "project_finance",
        ],
    }

    name = models.CharField(max_length=255)

    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    product_subtype = models.CharField(max_length=50, choices=PRODUCT_SUBTYPE_CHOICES)

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="client_policies")
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="staff_managed_policies")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_clients")

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    installment_frequency = models.CharField(max_length=20, choices=INSTALLMENT_CHOICES, default="monthly")
    duration_time = models.PositiveIntegerField(null=True, blank=True)
    start_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        # 🔒 Guard clause (important for partial forms / admin / updates)
        if not self.product_type or not self.product_subtype:
            return

        allowed_subtypes = self.PRODUCT_MAPPING.get(self.product_type, [])

        if self.product_subtype not in allowed_subtypes:
            raise ValidationError({
                "product_subtype": "Invalid product_subtype for selected product_type"
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures model validation always runs
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()}) - {self.client}"
