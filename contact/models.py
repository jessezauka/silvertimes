from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images import get_image_model_string


class ContactFormField(AbstractFormField):
    page = ParentalKey("contact.ContactPage", related_name="form_fields", on_delete=models.CASCADE)


class ContactPage(AbstractEmailForm):
    banner_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    intro_text = RichTextField(blank=True)
    form_intro_text = RichTextField(blank=True)

    # shown after successful submit (this was missing)
    thank_you_text = RichTextField(blank=True)

    # public contact info (optional)
    phone = models.CharField(max_length=50, blank=True)
    public_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    parent_page_types = ["home.HomePage"]
    subpage_types: list[str] = []

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("intro_text"),
        MultiFieldPanel(
            [FieldPanel("phone"), FieldPanel("public_email"), FieldPanel("address")],
            heading="Contact info",
        ),
        FieldPanel("form_intro_text"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [FieldPanel("to_address"), FieldPanel("from_address"), FieldPanel("subject")],
            heading="Email settings",
        ),
    ]
