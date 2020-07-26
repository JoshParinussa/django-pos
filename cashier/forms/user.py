"""User forms module."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from cashier.forms.base import CustomModelForm, CustomUserCreationForm

# from oree.forms.widgets import MetronicAvatar

User = get_user_model()


class DashUserCreationForm(CustomUserCreationForm):
    """Custom user creation form."""

    def save(self, *args, **kwargs):
        """Override save."""
        self.instance.is_staff = True
        return super().save(*args, **kwargs)

    class Meta:  # noqa D106
        model = User
        fields = ('email', 'username', 'password1', 'password2', )


class DashUserUpdateForm(CustomModelForm):
    """CmsUserUpdateForm."""
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password change"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password change confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        required=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 and password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        
        if password1 and not password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

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
