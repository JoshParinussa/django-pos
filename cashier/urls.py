"""Buildr url module."""
from django.urls import include, path
from rest_framework import routers

from cashier.views import dash as dash_view
from cashier.views.apis import product as api_product
from cashier.views.apis import category as api_category
from cashier.views.apis import unit as api_unit
from cashier.views.apis import user as api_user
from cashier.views.apis import supplier as api_supplier
from cashier.views.apis import sale as api_sale
from cashier.views.apis import income as api_income
from cashier.views.apis import expenses as api_expenses
from cashier.views.apis import invoice as api_invoice
from cashier.views.apis import purchase as api_purchase
from cashier.views.apis import purchase_detail as api_purchase_detail
from cashier.views.apis import member as api_member
from cashier.views.dash import account as account_view
from cashier.views.dash import product as dash_product_view
from cashier.views.dash import category as dash_category_view
from cashier.views.dash import unit as dash_unit_view
from cashier.views.dash import user as dash_user_view
from cashier.views.dash import supplier as dash_supplier_view
from cashier.views.dash import transaction as dash_transaction_view
from cashier.views.dash import purchase as dash_purchase_view
from cashier.views.dash import income as dash_income_view
from cashier.views.dash import expenses as dash_expenses_view
from cashier.views.dash import member as dash_member_view

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'sales', api_sale.SaleViewSet)
router.register(r'units', api_unit.UnitViewSet)
router.register(r'categories', api_category.ProductCategoryViewSet)
router.register(r'products', api_product.ProductViewSet)
router.register(r'report_out_of_stock', api_product.ReportOutOfStockViewSet)
router.register(r'converts', api_product.ConvertViewSet)
router.register(r'employees', api_user.UserViewSet)
router.register(r'supplier', api_supplier.SupplierViewSet)
router.register(r'income', api_income.IncomeViewSet)
router.register(r'expenses', api_expenses.ExpensesViewSet)
router.register(r'report_transaction', api_sale.ReportTransactionViewSet)
router.register(r'report_sale', api_sale.ReportSaleViewSet)
router.register(r'invoice', api_invoice.InvoiceViewSet)
router.register(r'purchase', api_purchase.PurchaseViewSet)
router.register(r'purchase_detail', api_purchase_detail.PurchaseDetailViewSet)
router.register(r'member', api_member.MemberViewSet)

urlpatterns = [
    path('v1/', include((router.urls, 'api_views'), namespace='v1')),

    path('', account_view.Login.as_view(), name='login'),
    path('logout', account_view.LogoutView.as_view(), name='dash_logout'),
    path('dash/', dash_view.DashHomeView.as_view(), name='dash_view'),

    # ADMIN UNIT
    path('dash/units', dash_unit_view.UnitListView.as_view(), name='dash_unit_list'),
    path('dash/units/create', dash_unit_view.UnitCreateView.as_view(), name='dash_unit_create'),
    path('dash/units/<str:pk>', dash_unit_view.UnitUpdateView.as_view(), name='dash_unit_update'),
    path('dash/units/<str:pk>/delete', dash_unit_view.UnitDeleteView.as_view(), name='dash_unit_delete'),

    # ADMIN CATEGORY
    path('dash/categories', dash_category_view.ProductCategoryListView.as_view(), name='dash_product_category_list'),
    path('dash/categories/create', dash_category_view.ProductCategoryCreateView.as_view(), name='dash_product_category_create'),
    path('dash/categories/<str:pk>', dash_category_view.ProductCategoryUpdateView.as_view(), name='dash_product_category_update'),
    path('dash/categories/<str:pk>/delete', dash_category_view.ProductCategoryDeleteView.as_view(), name='dash_product_category_delete'),

    # ADMIN PRODUCT
    path('dash/products', dash_product_view.ProductListView.as_view(), name='dash_product_list'),
    path('dash/products/create', dash_product_view.ProductCreateView.as_view(), name='dash_product_create'),
    path('dash/products/<str:pk>', dash_product_view.ProductUpdateView.as_view(), name='dash_product_update'),
    path('dash/products/<str:pk>/delete', dash_product_view.ProductDeleteView.as_view(), name='dash_product_delete'),
    path('dash/products/<str:pk>/converts/get_by_product', dash_product_view.ConvertBarangListView.as_view(), name='dash_convert_barang_list'),
    path('dash/products/<str:pk>/converts/create', dash_product_view.ConvertBarangCreateView.as_view(), name='dash_convert_barang_create'),
    path('dash/products/<str:product>/converts/<str:pk>', dash_product_view.ConvertBarangUpdateView.as_view(), name='dash_convert_barang_update'),
    path('dash/products/<str:product>/converts/<str:pk>/delete', dash_product_view.ConvertBarangDeleteView.as_view(), name='dash_convert_barang_delete'),

    # ADMIN SUPPLIER
    path('dash/supplier', dash_supplier_view.SupplierListView.as_view(), name='dash_supplier_list'),
    path('dash/supplier/create', dash_supplier_view.SupplierCreateView.as_view(), name='dash_supplier_create'),
    path('dash/supplier/<str:pk>', dash_supplier_view.SupplierUpdateView.as_view(), name='dash_supplier_update'),
    path('dash/supplier/<str:pk>/delete', dash_supplier_view.SupplierDeleteView.as_view(), name='dash_supplier_delete'),

    # MEMBER
    path('dash/member', dash_member_view.MemberListView.as_view(), name='dash_member_list'),
    path('dash/member/create', dash_member_view.MemberCreateView.as_view(), name='dash_member_create'),
    path('dash/member/<str:pk>', dash_member_view.MemberUpdateView.as_view(), name='dash_member_update'),
    path('dash/member/<str:pk>/delete', dash_member_view.MemberDeleteView.as_view(), name='dash_member_delete'),

    # EMPLOYEES
    path('dash/users', dash_user_view.UserListView.as_view(), name='dash_user_list'),
    path('dash/users/create', dash_user_view.UserCreateView.as_view(), name='dash_user_create'),
    path('dash/users/<str:pk>', dash_user_view.UserUpdateView.as_view(), name='dash_user_update'),
    path('dash/users/<str:pk>/delete', dash_user_view.UserDeleteView.as_view(), name='dash_user_delete'),

    # SALE
    path('dash/transaction/sale', dash_transaction_view.SaleTransactionListView.as_view(), name='dash_transaction_list'),
    path('dash/transaction/sale/new', dash_transaction_view.SaleTransactionView.as_view(), name='dash_transaction_create'),
    path('dash/transaction/sale/update/<str:pk>', dash_transaction_view.SaleTransactionView.as_view(), name='dash_report_transaction_detail'),
    
    # PURCHASE
    path('dash/transaction/purchase', dash_purchase_view.PurchaseListView.as_view(), name='dash_purchase_list'),
    path('dash/transaction/purchase/new', dash_purchase_view.PurchaseDetailView.as_view(), name='dash_purchase_create'),
    path('dash/transaction/purchase/update/<str:pk>', dash_purchase_view.PurchaseDetailView.as_view(), name='dash_purchase_detail'),

    # INCOME
    path('dash/transaction/income', dash_income_view.IncomeListView.as_view(), name='dash_income_list'),
    path('dash/transaction/income/create', dash_income_view.IncomeCreateView.as_view(), name='dash_income_create'),
    path('dash/transaction/income/<str:pk>', dash_income_view.IncomeUpdateView.as_view(), name='dash_income_update'),
    path('dash/transaction/income/<str:pk>/delete', dash_income_view.IncomeDeleteView.as_view(), name='dash_income_delete'),

    # EXPENSES
    path('dash/transaction/expenses', dash_expenses_view.ExpensesListView.as_view(), name='dash_expenses_list'),
    path('dash/transaction/expenses/create', dash_expenses_view.ExpensesCreateView.as_view(), name='dash_expenses_create'),
    path('dash/transaction/expenses/<str:pk>', dash_expenses_view.ExpensesUpdateView.as_view(), name='dash_expenses_update'),
    path('dash/transaction/expenses/<str:pk>/delete', dash_expenses_view.ExpensesDeleteView.as_view(), name='dash_expenses_delete'),

    #REPORTS
    path('dash/report/transaction', dash_transaction_view.ReportTransactionView.as_view(), name='dash_report_transaction'),
    path('dash/report/sale-product', dash_transaction_view.ReportSalebyProductView.as_view(), name='dash_report_sale_by_product'),
    path('dash/report/sale/<str:pk>', dash_transaction_view.ReportSaleView.as_view(), name='dash_report_sale'),
    path('dash/report/profit_loss', dash_transaction_view.ReportProfitLossView.as_view(), name='dash_report_profit_loss'),
    path('dash/report/product_out_of_stock',dash_product_view.ReportOutOfStockListView.as_view(),name='dash_report_out_of_stock')
]   
