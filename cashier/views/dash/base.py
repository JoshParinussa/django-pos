"""Base view module."""
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.text import camel_case_to_spaces, slugify
from django.views.generic import (CreateView, DeleteView, FormView,
                                  TemplateView, UpdateView, View)


class CustomCreateView(SuccessMessageMixin, CreateView):
    """CustomCreateView."""

    success_message = "Create success"


class CustomUpdateView(SuccessMessageMixin, UpdateView):
    """CustomUpdateView."""

    success_message = "Update success"


class CustomDeleteView(SuccessMessageMixin, DeleteView):
    """CustomDeleteView."""

    success_message = "%(id)s was deleted successfully"

    def delete(self, request, *args, **kwargs):
        """Override ride delete to pass success message."""
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(CustomDeleteView, self).delete(request, *args, **kwargs)


class CustomFormView(SuccessMessageMixin, FormView):
    """CustomFormView."""

    success_message = "Record was created successfully"


class CustomView(SuccessMessageMixin, View):
    """CustomFormView."""


class CmsCrudMixin:
    """CmsCrudMixin."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon2-cube'

    def get_model(self):
        """Get model."""
        if getattr(self, 'get_object', None) is not None:
            return self.get_object().__class__

        raise NotImplementedError

    def _get_url_name(self, action):
        """Get CRUD url name.

        format = cms_<model underscore name>_<action>
        action = [list, create, update, delete,]
        """
        s = slugify(camel_case_to_spaces(self.get_model().__name__))
        s = s.replace('-', '_')
        return f'dash_{s}_{action}'

    def get_actions(self):
        """Get type actions."""
        return ('create', 'update', 'list', 'delete')

    def get_current_action(self):
        """Get current page action, list, delete, update, create."""
        current_view_name = self.request.resolver_match.view_name
        return current_view_name.split('_')[-1]

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()

        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        return context

    def get_success_url(self):
        """Override get_success_url."""
        next = self.request.POST.get('next', None)
        if next == 'update':
            return reverse(self._get_url_name('update'), args=(self.object.pk,))
        elif next == 'create':
            return reverse(self._get_url_name('create'))
        else:
            return reverse(self._get_url_name('list'))


class DashListView(CmsCrudMixin, TemplateView):
    """DashListView."""
    model = None

    def get_model(self):
        """Get model representation of list."""
        if self.model:
            return self.model

        raise NotImplementedError()


class DashUpdateView(CmsCrudMixin, CustomUpdateView):
    """CmsUpdateView."""
    pass


class DashCreateView(CmsCrudMixin, CustomCreateView):
    """DashCreateView."""

    def get_model(self):
        """Get model representation of list."""
        if self.model:
            return self.model

        raise NotImplementedError()


class CmsDeleteView(CmsCrudMixin, CustomDeleteView):
    """CmsDeleteView."""
    pass


class DashCustomCreateView(CmsCrudMixin):
    """DashCreateView."""

    def get_model(self):
        """Get model representation of list."""
        if self.model:
            return self.model

        raise NotImplementedError()
