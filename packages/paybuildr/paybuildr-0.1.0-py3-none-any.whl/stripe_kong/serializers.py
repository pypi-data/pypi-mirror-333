from rest_framework import serializers
from .models import Plan, Subscription, PuckPage


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "amount", "currency", "interval", "stripe_price_id"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    
    class Meta:
        model = Subscription
        fields = ["id", "plan", "plan_name", "status", "current_period_end"]


class PuckPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuckPage
        fields = ["id", "title", "slug", "content", "published", "updated_at"]