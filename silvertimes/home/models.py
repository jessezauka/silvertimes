# home/models.py
from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

class HomePage(Page):
    banner_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )

    intro = RichTextField(blank=True)

    register_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    register_link_url = models.URLField(
        blank=True,
        help_text="Destination for the Register button (e.g. /reg/ or /accounts/signup/)"
    )

    max_count = 1

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("banner_image")], heading="Banner"),
        FieldPanel("intro"),
        MultiFieldPanel(
            [FieldPanel("register_image"), FieldPanel("register_link_url")],
            heading='"Create Your Account" section',
        ),
    ]

    def get_context(self, request):
        ctx = super().get_context(request)

        # Latest blog posts (use BlogPage.date)
        try:
            from blog.models import BlogPage
            ctx["latest_posts"] = (
                BlogPage.objects.live().public()
                .select_related("thumbnail", "banner_image")
                .order_by("-date")[:3]
            )
        except Exception:
            ctx["latest_posts"] = []

        # Latest galleries (no explicit date field -> use first_published_at)
        try:
            from galleries.models import GalleryPage
            ctx["latest_galleries"] = (
                GalleryPage.objects.live().public()
                .select_related("cover_image")
                .order_by("-first_published_at")[:3]
            )
        except Exception:
            ctx["latest_galleries"] = []

        return ctx
