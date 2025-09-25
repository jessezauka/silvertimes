# resources/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.search import index

from . import blocks as resource_blocks


class ResourcesPage(Page):
    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero image for the Resources page."
    )
    intro = models.TextField(blank=True, help_text="Shown centered under the title.")

    sections = StreamField(
        [
            ("resource", resource_blocks.ResourceItemBlock()),
            # You can add more block types later if you want (headings, text, etc.)
        ],
        use_json_field=True,
        blank=True,
    )

    subpage_types = []  # single page (no children)

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("intro"),
        FieldPanel("sections"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
    ]
