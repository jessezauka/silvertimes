# processes/models.py
from wagtail.fields import RichTextField, StreamField
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.html import strip_tags

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string
from wagtail.search import index
from . import blocks as process_blocks


class ProcessesIndexPage(Page):
    """
    Landing page that lists ProcessPage children (no categories).
    """
    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero image for the Processes landing."
    )
    intro = models.TextField(blank=True, help_text="Short blurb shown above the list.")
    paginate_by = models.PositiveIntegerField(default=10, help_text="Items per page.")

    subpage_types = ["processes.ProcessPage"]

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("intro"),
        FieldPanel("paginate_by"),
    ]

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)
        qs = (
            ProcessPage.objects
            .descendant_of(self)
            .live()
            .order_by("-date")
            .select_related("thumbnail", "banner_image")
            .specific()
        )
        paginator = Paginator(qs, self.paginate_by)
        page_num = request.GET.get("page")
        try:
            items = paginator.page(page_num)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        ctx["items"] = items
        return ctx


class ProcessPage(Page):
    date = models.DateField("Publication date")
    author_name = models.CharField(max_length=255, blank=True)

    thumbnail = models.ForeignKey(
        get_image_model_string(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        help_text="Thumbnail used on Processes listing."
    )
    banner_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )

    excerpt = models.TextField(
        blank=True,
        help_text="Short summary shown on the Processes index."
    )

    # Keep your simple body for free text
    body = RichTextField(blank=True, features=["h2","h3","bold","italic","link","ol","ul","hr","image","embed","code"])

    # NEW: sections to build the layout you pasted
    sections = StreamField([
        ("h2", process_blocks.Heading2Block()),
        ("paragraph", process_blocks.ParagraphBlock()),
        ("collapsible", process_blocks.CollapsibleBlock()),
        ("full_width_image", process_blocks.FullWidthImageBlock()),
        ("image_text_row", process_blocks.ImageTextRowBlock()),
        ("wrapped_image_text", process_blocks.WrappedImageTextBlock()),
    ], use_json_field=True, blank=True)

    parent_page_types = ["processes.ProcessesIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("date"),
            FieldPanel("author_name"),
        ], heading="Meta"),
        FieldPanel("thumbnail"), 
        FieldPanel("banner_image"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
        FieldPanel("sections"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.FilterField("date"),
        index.FilterField("author_name"),
    ]
