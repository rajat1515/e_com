from core.views import VendorCreation
from django.urls import path

urlpatterns = [
    path('vendor/', VendorCreation.as_view()),
]