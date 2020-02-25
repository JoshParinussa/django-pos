"""Base form module."""
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ModelForm


class CustomUserCreationForm(UserCreationForm):
    """CustomUserCreationForm."""

    def __init__(self, *args, **kwargs):
        """Re-init."""
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class CustomModelForm(ModelForm):
    """CustomModelForm."""

    def __init__(self, *args, **kwargs):
        """Re-init."""
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class CustomForm(Form):
    """CustomForm."""

    def __init__(self, *args, **kwargs):
        """Re-init."""
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
