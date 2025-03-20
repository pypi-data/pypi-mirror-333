from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Plan, Subscription, PuckPage
from .serializers import PlanSerializer, SubscriptionSerializer, PuckPageSerializer
from .utils.stripe_client import StripeClient

stripe_client = StripeClient()


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(active=True)
    serializer_class = PlanSerializer
    
    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):
        plan = self.get_object()
        success_url = request.data.get("success_url", settings.STRIPE_SUCCESS_URL)
        cancel_url = request.data.get("cancel_url", settings.STRIPE_CANCEL_URL)
        
        try:
            mode = "subscription" if plan.interval != "once" else "payment"
            session = stripe_client.create_checkout_session(
                plan.stripe_price_id,
                success_url,
                cancel_url,
                customer_email=request.user.email if request.user.is_authenticated else None,
                client_reference_id=str(request.user.id) if request.user.is_authenticated else None,
                mode=mode
            )
            return Response({"id": session.id, "url": session.url})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Subscription.objects.filter(user=self.request.user)
        return Subscription.objects.none()


class PuckPageViewSet(viewsets.ModelViewSet):
    queryset = PuckPage.objects.filter(published=True)
    serializer_class = PuckPageSerializer
    lookup_field = "slug"


def page_view(request, slug):
    page = get_object_or_404(PuckPage, slug=slug, published=True)
    context = {
        "page": page,
        "content": page.content,
    }
    return render(request, "stripe_kong/page.html", context)


@csrf_exempt
def stripe_webhook(request):
    # Process Stripe webhook events
    # Implementation depends on webhook events you want to handle
    pass