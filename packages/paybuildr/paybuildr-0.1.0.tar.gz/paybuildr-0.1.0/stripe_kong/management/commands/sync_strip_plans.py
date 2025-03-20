import stripe
from django.conf import settings
from typing import Optional, Union, Dict, Any

class StripeClient:
    def __init__(self):
        self.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = self.api_key
    
    def create_product(self, name: str) -> stripe.Product:
        """Create a new product in Stripe"""
        return stripe.Product.create(name=name)
    
    def create_price(
        self, 
        product_id: str, 
        unit_amount: int, 
        currency: str, 
        interval: Optional[str] = None
    ) -> stripe.Price:
        """Create a new price for a product in Stripe"""
        price_data: Dict[str, Any] = {
            "product": product_id,
            "unit_amount": unit_amount,
            "currency": currency,
        }
        
        if interval:
            price_data["recurring"] = {"interval": interval}
        
        return stripe.Price.create(**price_data)
    
    def create_checkout_session(
        self, 
        price_id: str, 
        success_url: str, 
        cancel_url: str, 
        customer_email: Optional[str] = None,
        client_reference_id: Optional[str] = None,
        mode: str = "payment"
    ) -> stripe.checkout.Session:
        """Create a Stripe checkout session"""
        session_data: Dict[str, Any] = {
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
    
    def retrieve_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Retrieve subscription details from Stripe"""
        return stripe.Subscription.retrieve(subscription_id)
    
    def cancel_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Cancel a subscription in Stripe"""
        return stripe.Subscription.delete(subscription_id)