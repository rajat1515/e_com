from django.urls import path
from store.views import (UserManagementView,
                         StoreManagementView,
                         AddProductView,
                         UploadCSVView,
                         ProductSoldView,
                         CustomerRegistrationView,
                         ProductsView)

urlpatterns = [
    path('users/', UserManagementView.as_view()),
    path('stores/', StoreManagementView.as_view()),
    path('products/', ProductsView.as_view()),
    path('product_add/', AddProductView.as_view()),
    path('product_csv/', UploadCSVView.as_view()),
    path('product_sold/', ProductSoldView.as_view()),
    path('customer/', CustomerRegistrationView.as_view()),


]
