from django.db import models

from clients_app.models import ClientProfile
from policies_app.models import Policy


# Create your models here.
class Document(models.Model):
    DOCTYPE = (
        ("Identity Document","IDENTITY"),
        ("Financial Document","FINANCIAL"),
        ("Policy Document","POLICY"),
        ("Payment Document","PAYMENT"),
    )
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="documents")
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True, blank=True)

    document_type = models.CharField(max_length=20, choices=DOCTYPE)

    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.document_type}"
