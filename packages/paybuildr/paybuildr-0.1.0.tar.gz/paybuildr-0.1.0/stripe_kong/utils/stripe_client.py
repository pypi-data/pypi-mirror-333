import stripe
from django.conf import settings

class StripeClient:
    def __init__(self):
        self.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = self.api_key
    
    def create_product(self, name):
        return stripe.Product.create(name=name)
    
    def create_price(self, product_id, unit_amount, currency, interval=None):
        price_data = {
            "product": product_id,
            "unit_amount": unit_amount,
            "currency": currency,
        }
        
        if interval:
            price_data["recurring"] = {"interval": interval}
        
        return stripe.Price.create(**price_data)
    
    def create_checkout_session(self, price_id, success_url, cancel_url, customer_email=None, client_reference_id=None, mode="payment"):
        session_data = {
            "payment_method_types": ["card"],
            "line_items": [{"price": price_id, "quantity": 1}],
            "mode": mode,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }
        
        if customer_email:
            session_data["customer_email"] = customer_email
            
        if client_reference_id:
            session_data["client_reference_id"] = client_reference_id
            
        return stripe.checkout.Session.create(**session_data)