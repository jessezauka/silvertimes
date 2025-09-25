from django.db import models
from django.contrib.auth import get_user_model
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
import uuid

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Customer Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Address
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='Ireland')
    
    # Payment Info (simplified - use proper payment processor in production)
    card_holder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)  # Should be encrypted in production
    expiry_date = models.CharField(max_length=7, help_text="MM/YYYY")
    cvv = models.CharField(max_length=4)
    
    # Order Details
    order_details = models.TextField(help_text="What to print")
    special_instructions = models.TextField(blank=True)
    
    # System Fields
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"

class PrintshopPage(Page):
    intro = RichTextField(blank=True)
    services = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('services'),
    ]
    
    template = "printshop/printshop_page.html"