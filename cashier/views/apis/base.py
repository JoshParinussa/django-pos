"""Base api view module."""
from rest_framework.settings import api_settings
from rest_framework import viewsets


class APIBaseView(viewsets.ModelViewSet):
    """APIBaseView."""
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
