from django.db import models


# Create your models here.

class ProductType(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ("loan", "Loan"),
        ("insurance", "Insurance"),
        ("finance", "Finance"),
    )
    name = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default="loan")

    def __str__(self):
        return self.name


class ProductSubType(models.Model):
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

    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="sub_types")
    name = models.CharField(max_length=50, choices=PRODUCT_SUB_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.product_type.name} - {self.name}"
