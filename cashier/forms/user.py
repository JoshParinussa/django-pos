"""User forms module."""
from django.contrib.auth import get_user_model

from cashier.forms.base import CustomModelForm, CustomUserCreationForm

# from oree.forms.widgets import MetronicAvatar

User = get_user_model()


class DashUserCreationForm(CustomUserCreationForm):
    """Custom user creation form."""

    # def save(self, *args, **kwargs):
    #     """Override save."""
    #     self.instance.username = self.instance.email
    #     return super().save(*args, **kwargs)

    class Meta:  # noqa D106
        model = User
        fields = ('email', 'username', 'password1', 'password2', )


class DashUserUpdateForm(CustomModelForm):
    """CmsUserUpdateForm."""
    class Meta:  # noqa D106
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', )
        # widgets = {
        #     'picture': MetronicAvatar(),
        # }


class ProfileUpdateForm(CustomModelForm):
    """ProfileUpdateForm."""
    class Meta:  # noqa D106
        model = User
        fields = ('first_name', 'last_name', )
        # widgets = {
        #     'picture': MetronicAvatar(),
        # }
