"""Product views."""
from cashier.forms import product as product_forms
from cashier.forms import product as product_forms
from cashier.models import Product
from cashier.views.dash.base import DashCreateView, DashListView, DashCustomCreateView, DashUpdateView
from django.shortcuts import render
from django.views.generic import View

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
    """ProductCreateView."""
    model = Product
    form_class = product_forms.DashProductCreationForm
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
