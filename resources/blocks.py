# resources/blocks.py
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class ResourceItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Small logo/icon for the resource")
    title = blocks.CharBlock()
    summary = blocks.TextBlock(required=False, help_text="Short description shown under the title")
    url = blocks.URLBlock(label="Link URL")
    link_label = blocks.CharBlock(required=False, default="Explore")
    open_in_new_tab = blocks.BooleanBlock(required=False, default=True, help_text="Open link in a new tab")

    class Meta:
        icon = "site"
        template = "resources/blocks/resource_item.html"
