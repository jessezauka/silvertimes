from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images import get_image_model_string
from wagtail.search import index
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


class GalleriesIndexPage(Page):
    """Lists all GalleryPage children."""
    intro = RichTextField(blank=True)

    # adjust 'home.HomePage' if your home page class differs
    parent_page_types = ["home.HomePage"]
    subpage_types = ["galleries.GalleryPage"]
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        ctx = super().get_context(request)
        qs = GalleryPage.objects.child_of(self).live().public()
        ctx["galleries"] = qs
        return ctx

class GalleryPage(Page):
    """One gallery with many images (orderable)."""
    intro = RichTextField(blank=True)
    cover_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    parent_page_types = ["galleries.GalleriesIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
        FieldPanel("intro"),
        InlinePanel("images", label="Images"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("intro"),
    ]

class GalleryImage(Orderable):
    """Inline image for a GalleryPage."""
    page = ParentalKey("galleries.GalleryPage", related_name="images", on_delete=models.CASCADE)
    image = models.ForeignKey(get_image_model_string(), on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("alt_text"),
    ]

@register_setting
class SiteFooterSettings(BaseSiteSetting):
    footer_html = RichTextField(
        features=["bold", "italic", "link"],  # adjust toolbar as you like
        default="© 2025 SilverTimes.ART. All rights reserved.",
        help_text="Shown in the site footer",
        # validators=[MaxLengthValidator(500)],  # optional; counts HTML too
    )

    panels = [FieldPanel("footer_html")]
