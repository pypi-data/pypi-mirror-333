# apps/payments/admin.py
from django.contrib import admin
import stripe
from django.conf import settings
from .models import Plan, Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'currency', 'interval', 'active')
    search_fields = ('name',)
    list_filter = ('interval', 'active')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new plan
            # Create the price in Stripe
            stripe_product = stripe.Product.create(name=obj.name)
            
            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(obj.amount * 100),
                currency=obj.currency,
                recurring={"interval": obj.interval} if obj.interval != 'once' else None,
            )
            
            obj.stripe_price_id = stripe_price.id
            
        super().save_model(request, obj, form, change)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'current_period_end')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email')