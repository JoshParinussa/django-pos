"""Product views."""
from cashier.forms import product as product_forms
from cashier.models import Product, ConvertBarang
from cashier.views.dash.base import DashCreateView, DashListView, DashCustomCreateView, DashUpdateView
from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse

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
    form_class = product_forms.DashProductCreationForm
    template_name = 'dash/product/create.html'


class ProductUpdateView(DashProductMixin, DashUpdateView):
    """ProductUpdateView."""
    model = Product
    form_class = product_forms.DashProductUpdateForm
    template_name = 'dash/product/update.html'


class NewProductCreateView(DashProductMixin, DashCustomCreateView, View):
    """ProductCreateView."""
    template_name = 'dash/product/create.html'
    model = Product

    def get(self, request):
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

