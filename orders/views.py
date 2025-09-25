from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from .forms import OrderForm
from wagtail.models import Page

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'  # Change this line - was probably 'printshop/order_form.html'
    
    def form_valid(self, form):
        # Save the order
        order = form.save(commit=False)
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order.save()
        
        # Send confirmation email (optional)
        try:
            send_mail(
                subject=f'Order Confirmation - {order.id}',
                message=f'''
                Dear {order.first_name},
                
                Thank you for your order! We've received your printing request.
                
                Order ID: {order.id}
                Order Details: {order.order_details}
                
                We'll process your order and get back to you soon.
                
                Best regards,
                SilverTimes Printshop
                ''',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@silvertimes.com'),
                recipient_list=[order.email],
                fail_silently=True,
            )
        except Exception:
            pass  # Email failed, but order still succeeded
        
        messages.success(self.request, f'Order submitted successfully! Order ID: {order.id}')
        return redirect('orders:order_success', order_id=order.id)

    def get_initial(self):
        initial = super().get_initial()
        item_id = self.request.GET.get('item_id')
        if item_id:
            try:
                page = Page.objects.get(id=item_id).specific
                price = getattr(page, 'price_label', '')
                suffix = f" - €{price}" if price else ""
                initial['order_details'] = f"{page.title}{suffix}"
            except Page.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.request.GET.get('item_id')
        context['item_page'] = None
        if item_id:
            try:
                page = Page.objects.get(id=item_id).specific
                context['item_page'] = page
                context['item_title'] = page.title
                context['item_price'] = getattr(page, 'price_label', None)
                context['item_image'] = getattr(page, 'main_image', None)
            except Page.DoesNotExist:
                pass
        return context

class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['order'] = Order.objects.get(id=kwargs['order_id'])
        except Order.DoesNotExist:
            context['order'] = None
        return context