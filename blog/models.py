from django.db import models
from django.utils.text import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.models import Image
from modelcluster.fields import ParentalManyToManyField
from wagtail.images import get_image_model_string
from django.utils.functional import cached_property


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name_plural = "Blog categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class BlogIndexPage(Page):
    """
    Landing page that lists BlogPage children, with optional banner.
    """
    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero image for the blog landing."
    )
    paginate_by = models.PositiveIntegerField(default=10, help_text="Posts per page.")

    # Only allow BlogPage underneath this page
    subpage_types = ["blog.BlogPage"]

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("paginate_by"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        posts = (
            BlogPage.objects
            .descendant_of(self)
            .live()
            .order_by("-date")  # newest first
            .select_related("thumbnail", "banner_image")
            .prefetch_related("categories")
        )

        # Optional: filter by ?category=slug
        category_slug = request.GET.get("category")
        if category_slug:
            posts = posts.filter(categories__slug=category_slug)

        paginator = Paginator(posts, self.paginate_by)
        page_num = request.GET.get("page")
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context["posts"] = page_obj
        context["categories"] = BlogCategory.objects.all()
        context["current_category"] = category_slug
        return context


class BlogPage(Page):
    """
    Individual blog article.
    """
    date = models.DateField("Publication date")
    author_name = models.CharField(max_length=255, help_text="Shown on the index ‘by …’ line.")
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True, related_name="blog_pages")

    @cached_property
    def listing_image(self):
        # Prefer the square/landscape thumbnail; fall back to hero
        return self.thumbnail or self.banner_image

    # Listing thumbnail
    thumbnail = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Square/landscape thumbnail for listings."
    )

    # Optional hero per post
    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional hero image on the article page."
    )

    # Text fields
    excerpt = models.TextField(blank=True, help_text="Short summary shown on index. If blank, we’ll derive from body.")
    body = RichTextField(features=[
        "h2", "h3", "bold", "italic", "link", "ol", "ul", "hr", "image", "embed", "code"
    ])

    # Only allowed under BlogIndex; no children under a post
    parent_page_types = ["blog.BlogIndexPage"]
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
        FieldPanel("categories"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("excerpt"),
        index.SearchField("body"),
        index.FilterField("date"),
        index.FilterField("author_name"),
    ]

    @property
    def display_excerpt(self):
        # Provide a fallback if author didn’t write an excerpt
        if self.excerpt:
            return self.excerpt
        # crude fallback; for more control you can strip HTML or use a custom method
        return (self.body or "")[:240]
