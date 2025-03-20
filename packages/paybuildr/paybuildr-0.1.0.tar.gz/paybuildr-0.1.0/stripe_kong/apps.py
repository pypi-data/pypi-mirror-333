from django.apps import AppConfig

class StripeKongConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe_kong"
    verbose_name = "Stripe & Kong Integration"
    
    def ready(self):
        try:
            import stripe_kong.signals
        except ImportError:
            pass