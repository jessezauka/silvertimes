from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    path("success/<uuid:order_id>/", views.OrderSuccessView.as_view(), name="order_success"),
]