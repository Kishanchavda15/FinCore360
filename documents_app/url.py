from django.urls import path

from documents_app.views import (
    DocumentListCreateAPI,
    DocumentRetrieveUpdateDeleteAPI
)

Documents_Urls = [
    path("document/", DocumentListCreateAPI.as_view(), name="document-create-list"),
    path("document/<int:pk>/", DocumentRetrieveUpdateDeleteAPI.as_view(), name="document-detail"),
]