from django import template
from wagtail.models import Page

register = template.Library()

@register.simple_tag
def get_navigation_pages():
    # adjust to your needs (order, filters, specific())
    return Page.objects.live().public().in_menu()