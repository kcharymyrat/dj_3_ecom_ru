from django.urls import path

from .views import ProductDetailView

app_name = "mainapp"
urlpatterns = [
    path(
        "products/<str:ct_model>/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
]
