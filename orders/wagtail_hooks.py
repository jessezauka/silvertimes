from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from .models import Order

class OrderViewSet(ModelViewSet):
    model = Order
    menu_label = "Orders"
    icon = "form"
    add_to_admin_menu = True
    menu_order = 200

    # List view
    list_display = ["id", "first_name", "last_name", "email", "status", "created_at"]
    list_filter = ["status", "created_at", "country"]
    search_fields = ["id", "first_name", "last_name", "email", "order_details"]

    # Edit view: choose which fields are editable
    form_fields = [
        "first_name", "last_name", "email", "phone",
        "street_address", "city", "state", "zip_code", "country",
        "order_details", "special_instructions",
        "status", "total_amount",
    ]

    # Optional: nicer grouping on the edit form
    panels = [
        MultiFieldPanel([
            FieldPanel("first_name"),
            FieldPanel("last_name"),
            FieldPanel("email"),
            FieldPanel("phone"),
        ], heading="Customer Information"),

        MultiFieldPanel([
            FieldPanel("street_address"),
            FieldPanel("city"),
            FieldPanel("state"),
            FieldPanel("zip_code"),
            FieldPanel("country"),
        ], heading="Shipping Address"),

        MultiFieldPanel([
            FieldPanel("order_details"),
            FieldPanel("special_instructions"),
        ], heading="Order Details"),

        MultiFieldPanel([
            FieldPanel("status"),
            FieldPanel("total_amount"),
        ], heading="Order Management"),
    ]

    # Read-only full details via Inspect view
    inspect_view_enabled = True
    inspect_view_fields = [
        "id",
        "first_name", "last_name", "email", "phone",
        "street_address", "city", "state", "zip_code", "country",
        "order_details", "special_instructions",
        # Payment fields kept for viewing only (consider removing from your model in production)
        "card_holder_name", "card_number", "expiry_date", "cvv",
        "status", "total_amount",
        "created_at", "updated_at",
    ]

@hooks.register("register_admin_viewset")
def register_order_viewset():
    return OrderViewSet("orders")