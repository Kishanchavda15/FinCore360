from django.contrib import admin

from documents_app.models import Document


# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "policy",
        "document_type",
        "file",
        "uploaded_at"
    ]
    search_fields = ["client__email"]