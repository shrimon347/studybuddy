from django.urls import path
from . import views
from .views import CreateStripeCheckoutSessionView,CancelView, SuccessView
from .views import StripeWebhookView


app_name = "products"

urlpatterns = [

    path("", views.ProductListView, name="product-list"),
    path("<int:pk>/", views.ProductDetailView, name="product-detail"),
    path(
        "create-checkout-session/<int:pk>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("success/", views.SuccessView, name="success"),
    path("cancel/", views.CancelView, name="cancel"),
]