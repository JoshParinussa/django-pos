"""Buildr url module."""
from django.urls import include, path
from rest_framework import routers

from cashier.views import dash as dash_view
from cashier.views.apis import product as api_product
from cashier.views.apis import category as api_category
from cashier.views.apis import unit as api_unit
from cashier.views.apis import user as api_user
from cashier.views.apis import supplier as api_supplier
from cashier.views.dash import account as account_view
from cashier.views.dash import product as dash_product_view
from cashier.views.dash import category as dash_category_view
from cashier.views.dash import unit as dash_unit_view
from cashier.views.dash import user as dash_user_view
from cashier.views.dash import supplier as dash_supplier_view
from cashier.views.dash import transaction as dash_transaction_view

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'units', api_unit.UnitViewSet)
router.register(r'categories', api_category.ProductCategoryViewSet)
router.register(r'products', api_product.ProductViewSet)
router.register(r'converts', api_product.ConvertViewSet)
router.register(r'employees', api_user.UserViewSet)
router.register(r'supplier', api_supplier.SupplierViewSet)
urlpatterns = [
    path('v1/', include((router.urls, 'api_views'), namespace='v1')),

    path('', account_view.Login.as_view(), name="login"),
    path('logout', account_view.LogoutView.as_view(), name="dash_logout"),
    path('dash/',
         dash_view.DashHomeView.as_view(),
         name='dash_view'),

    # ADMIN UNIT
    path('dash/units', dash_unit_view.UnitListView.as_view(), name='dash_unit_list'),
    path('dash/units/create', dash_unit_view.UnitCreateView.as_view(), name='dash_unit_create'),
    path('dash/units/<str:pk>', dash_unit_view.UnitUpdateView.as_view(), name='dash_unit_update'),

    # ADMIN CATEGORY
    path('dash/categories', dash_category_view.ProductCategoryListView.as_view(), name='dash_product_category_list'),
    path('dash/categories/create', dash_category_view.ProductCategoryCreateView.as_view(), name='dash_product_category_create'),
    path('dash/categories/<str:pk>', dash_category_view.ProductCategoryUpdateView.as_view(), name='dash_product_category_update'),

    # ADMIN PRODUCT
    path('dash/products', dash_product_view.ProductListView.as_view(), name='dash_product_list'),
    path('dash/products/create', dash_product_view.ProductCreateView.as_view(), name='dash_product_create'),
    path('dash/products/<str:pk>', dash_product_view.ProductUpdateView.as_view(), name='dash_product_update'),
    path('dash/products/<str:pk>/converts/get_by_product', dash_product_view.ConvertBarangListView.as_view(), name='dash_convert_barang_list'),
    path('dash/products/<str:pk>/converts/create', dash_product_view.ConvertBarangCreateView.as_view(), name='dash_convert_barang_create'),

    # ADMIN SUPPLIER
    path('dash/supplier', dash_supplier_view.SupplierListView.as_view(), name='dash_supplier_list'),
    path('dash/supplier/create', dash_supplier_view.SupplierCreateView.as_view(), name='dash_supplier_create'),
    path('dash/supplier/<str:pk>', dash_supplier_view.SuplierUpdateView.as_view(), name='dash_supplier_update'),

    # EMPLOYEES
    path('dash/users', dash_user_view.UserListView.as_view(), name='dash_user_list'),
    path('dash/users/create', dash_user_view.UserCreateView.as_view(), name='dash_user_create'),
    path('dash/users/<str:pk>', dash_user_view.UserUpdateView.as_view(), name='dash_user_update'),
    path('dash/users/<str:pk>/delete', dash_user_view.UserDeleteView.as_view(), name='dash_user_delete'),

    # TRANSACTION
    path('dash/transaction/sale', dash_transaction_view.SaleTransactionView.as_view(), name='dash_transaction_create'),
]
