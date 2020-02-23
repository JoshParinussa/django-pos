"""Admin view."""
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class AdminHomeView(TemplateView):
    """Home view."""
    template_name = "index.html"
