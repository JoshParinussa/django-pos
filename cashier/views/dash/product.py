"""Product views."""
from cashier.forms import product as product_forms
from cashier.forms.product import HargaBertingkatFormset
from cashier.models import Product, ConvertBarang, HargaBertingkat
from cashier.views.dash.base import DashCreateView, DashListView, DashCustomCreateView, DashUpdateView, DashDeleteView
from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect


class DashProductMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class ProductListView(DashProductMixin, DashListView):
    """BrandListView."""
    template_name = 'dash/product/list.html'
    model = Product


class ProductCreateView(DashProductMixin, DashCreateView):
    """ProductCreateView."""
    model = Product
    form_class = product_forms.DashProductForm
    template_name = 'dash/product/create copy.html'

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

        if self.request.POST:
            context['harga_bertingkat_formset'] = HargaBertingkatFormset(self.request.POST)
        else:
            context['harga_bertingkat_formset'] = HargaBertingkatFormset(queryset=HargaBertingkat.objects.none())
            

        return context

    def form_valid(self, form):
        """Override form valid."""
        context = self.get_context_data()
        harga_bertingkat_formset = context['harga_bertingkat_formset']
        product = form.save()

        if harga_bertingkat_formset.is_valid():
            for frm in harga_bertingkat_formset:
                if frm.has_changed():
                    harga_bertingkat = frm.save(commit=False)
                    harga_bertingkat.product = product
                    harga_bertingkat.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductUpdateView(DashProductMixin, DashUpdateView):
    """ProductUpdateView."""
    model = Product
    form_class = product_forms.DashProductForm
    template_name = 'dash/product/update.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        harga_bertingkat_queryset = self.object.hargabertingkat.order_by('created_at')
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()

        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        if self.request.POST:
            context['harga_bertingkat_formset'] = HargaBertingkatFormset(self.request.POST)
        else:
            context['harga_bertingkat_formset'] = HargaBertingkatFormset(queryset=harga_bertingkat_queryset)

        return context

    def form_valid(self, form):
        """Override form valid."""
        context = self.get_context_data()
        harga_bertingkat_formset = context['harga_bertingkat_formset']
        product = form.save()

        if harga_bertingkat_formset.is_valid():
            for frm in harga_bertingkat_formset:
                print("#HRg", frm)
                if frm.has_changed():
                    harga_bertingkat = frm.save(commit=False)
                    harga_bertingkat.product = product
                    harga_bertingkat.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductDeleteView(DashProductMixin, DashDeleteView):
    """ProductDeleteView."""
    model = Product
    template_name = 'dash/product/delete.html'


class NewProductCreateView(DashProductMixin, DashCustomCreateView, View):
    """ProductCreateView."""
    template_name = 'dash/product/create.html'
    model = Product

    def get(self, request):
        """Get."""
        if request.method == "POST":
            product_form = product_forms.DashProductCreationForm(request.POST)
            harga_bertingkat_form = [product_forms.DashHargaBertingkatCreationForm(prefix=str(x)) for x in range(3)]
            # harga_bertingkat_form = product_forms.DashHargaBertingkatCreationForm(request.POST)

            if product_form.is_valid() and harga_bertingkat_form.is_valid():
                product = product_form.save()
                harga_bertingkat = harga_bertingkat_form.save(False)

                harga_bertingkat.product = product
                harga_bertingkat.save()
        else:
            product_form = product_forms.DashProductCreationForm
            harga_bertingkat_form = product_forms.DashHargaBertingkatCreationForm

        context = {
            'product_form': product_form,
            'harga_bertingkat_form': harga_bertingkat_form,
            'tes': "TES"
        }

        return render(request, self.template_name, context)


def product_create(request):
    """Product_create."""
    template_name = 'dash/product/create.html'
    if request.method == "POST":
        product_form = product_forms.DashProductCreationForm(request.POST)
        harga_bertingkat_form = [product_forms.DashHargaBertingkatCreationForm(prefix=str(x)) for x in range(3)]
        # harga_bertingkat_form = product_forms.DashHargaBertingkatCreationForm(request.POST)

        if product_form.is_valid() and harga_bertingkat_form.is_valid():
            product = product_form.save()
            harga_bertingkat = harga_bertingkat_form.save(False)

            harga_bertingkat.product = product
            harga_bertingkat.save()
    else:
        product_form = product_forms.DashProductCreationForm
        harga_bertingkat_form = product_forms.DashHargaBertingkatCreationForm

    context = {
        'product_form': product_form,
        'harga_bertingkat_form': harga_bertingkat_form,
        'tes': "TES"
    }

    return render(request, template_name, context)


class ConvertBarangListView(DashProductMixin, DashListView):
    """ConvertBarangListView."""
    template_name = 'dash/convert/list.html'
    model = ConvertBarang

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()
        object_product = Product.objects.filter(id=self.kwargs.get('pk'))
        context['product_name'] = object_product.first().name
        context['product_id'] = self.kwargs.get('pk')

        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        return context


class ConvertBarangCreateView(DashProductMixin, DashCreateView):
    """ConvertBarangCreateView."""
    model = ConvertBarang
    form_class = product_forms.DashConvertBarangCreationForm
    template_name = 'dash/convert/create.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()
        object_product = Product.objects.filter(id=self.kwargs.get('pk'))
        context['product_name'] = object_product.first().name
        context['product_id'] = self.kwargs.get('pk')

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
            return reverse(self._get_url_name('list'), args=(self.kwargs.get('pk'),))


class ConvertBarangUpdateView(DashProductMixin, DashUpdateView):
    """ConvertBarangUpdateView."""
    model = ConvertBarang
    form_class = product_forms.DashConvertBarangUpdateForm
    template_name = 'dash/convert/update.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()
        object_product = Product.objects.filter(id=self.kwargs.get('product'))
        context['product_name'] = object_product.first().name
        context['product_id'] = self.kwargs.get('product')

        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        return context

    def get_success_url(self):
        """Override get_success_url."""
        action = self.request.POST.get('next', None)
        if action == 'update':
            return reverse(self._get_url_name('update'), args=(self.object.pk,))
        elif action == 'create':
            return reverse(self._get_url_name('create'))
        else:
            return reverse(self._get_url_name('list'), args=(self.kwargs.get('product'),))


class ConvertBarangDeleteView(DashProductMixin, DashDeleteView):
    """ConvertBarangDeleteView."""
    model = ConvertBarang
    template_name = 'dash/convert/delete.html'

    def get_context_data(self, **kwargs):
        """Override get context."""
        model = self.get_model()
        context = super().get_context_data(**kwargs)
        context['model_name'] = model._meta.verbose_name.title()
        context['model_name_plural'] = model._meta.verbose_name_plural.title()
        context['icon'] = self.get_icon()
        context['action'] = self.get_current_action()
        object_product = Product.objects.filter(id=self.kwargs.get('product'))
        context['product_name'] = object_product.first().name
        context['product_id'] = self.kwargs.get('product')
        context['object_id'] = self.kwargs.get('pk')
        print("#TES", self.kwargs.get('pk'))

        for action in self.get_actions():
            url_name = self._get_url_name(action)
            context[f'{action}_url_name'] = url_name

        return context

    def get_success_url(self):
        """Override get_success_url."""
        next = self.request.POST.get('next', None)
        if next == 'update':
            # return reverse(self._get_url_name('update'), args=(self.object.pk,))
            return reverse(self._get_url_name('update'), kwargs={'product_id': self.kwargs.get('product'), 'pk': self.object.pk})
        elif next == 'create':
            return reverse(self._get_url_name('create'))
        else:
            return reverse(self._get_url_name('list'), args=(self.kwargs.get('product'),))
