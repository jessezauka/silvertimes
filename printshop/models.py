# printshop/models.py
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string

class PrintshopIndexPage(Page):
    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = RichTextField(blank=True)

    parent_page_types = ["home.HomePage"]            # adjust if your Home class differs
    subpage_types = ["printshop.PrintshopItemPage"]

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        ctx = super().get_context(request)
        items = PrintshopItemPage.objects.child_of(self).live().public()
        ctx["items"] = items
        return ctx


class PrintshopItemPage(Page):
    main_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    format = models.CharField(max_length=120, blank=True)
    technique = models.CharField(max_length=160, blank=True)
    date_created = models.DateField(null=True, blank=True)
    short_description = RichTextField(blank=True)
    description = RichTextField(blank=True)

    price_label = models.CharField(max_length=120, blank=True)
    order_cta_text = models.CharField(max_length=60, blank=True, default="Order")
    order_target_url = models.URLField(blank=True)

    parent_page_types = ["printshop.PrintshopIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("main_image"),
        MultiFieldPanel([
            FieldPanel("format"),
            FieldPanel("technique"),
            FieldPanel("date_created"),
            FieldPanel("price_label"),
        ], heading="Print Details"),
        FieldPanel("short_description"),
        FieldPanel("description"),
        MultiFieldPanel([
            FieldPanel("order_cta_text"),
            FieldPanel("order_target_url"),
        ], heading="Ordering"),
    ]
