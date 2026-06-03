from django.db import models

from accounts_app.models import StaffProfile
from clients_app.models import ClientProfile


# Create your models here.
class PolicyType(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ("loan", "Loan"),
        ("insurance", "Insurance"),
        ("finance", "Finance"),
    )
    name = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default="loan")

    def __str__(self):
        return self.name


class PolicySubType(models.Model):
    PRODUCT_SUB_TYPE_CHOICES = (
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

    product_type = models.ForeignKey(PolicyType, on_delete=models.CASCADE, related_name="sub_types")
    name = models.CharField(max_length=50, choices=PRODUCT_SUB_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.product_type.name} - {self.name}"

class Policy(models.Model):
    STATUS_CHOICES = (
        ("Active", "ACTIVE"),
        ("Completed", "COMPLETED"),
    )
    INSTALLMENT_CHOICES = (
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("half_yearly", "Half-Yearly"),
        ("yearly", "Yearly")
    )
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="client_policies")
    staff = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL,null=True, related_name="staff_managed_policies")

    policy_type = models.ForeignKey(PolicyType, on_delete=models.SET_NULL,null=True, related_name="product_type")
    policy_sub_type = models.ForeignKey(PolicySubType, on_delete=models.SET_NULL,null=True, related_name="product_subtype")

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    installment_frequency = models.CharField(max_length=20, choices=INSTALLMENT_CHOICES, default="monthly")
    duration_time = models.PositiveIntegerField(null=True, blank=True)


    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.policy_type.name} - {self.client.user.full_name}"
