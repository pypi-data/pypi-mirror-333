# apps/payments/views.py
import stripe
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(active=True)
    serializer_class = PlanSerializer
    
    @action(detail=True, methods=['post'])
    def create_checkout(self, request, pk=None):
        plan = self.get_object()
        success_url = request.data.get('success_url', settings.STRIPE_SUCCESS_URL)
        cancel_url = request.data.get('cancel_url', settings.STRIPE_CANCEL_URL)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription' if plan.interval != 'once' else 'payment',
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=str(request.user.id) if request.user.is_authenticated else None,
            )
            return Response({'id': checkout_session.id, 'url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=400)