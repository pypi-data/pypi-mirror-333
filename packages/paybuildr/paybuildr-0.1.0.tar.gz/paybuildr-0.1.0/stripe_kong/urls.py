from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from . import admin_views

router = DefaultRouter()
router.register(r"plans", views.PlanViewSet)
router.register(r"subscriptions", views.SubscriptionViewSet, basename="subscription")
router.register(r"pages", views.PuckPageViewSet)

app_name = "stripe_kong"

urlpatterns = [
    path("api/", include(router.urls)),
    path("webhook/", views.stripe_webhook, name="webhook"),
    path("page/<slug:slug>/", views.page_view, name="page_view"),

    # Admin views
    path("admin/kong-status/", admin_views.kong_status, name="kong_status"),
    path("admin/sync-service/<int:service_id>/", admin_views.sync_api_service, name="sync_api_service"),
    path("admin/sync-route/<int:route_id>/", admin_views.sync_api_route, name="sync_api_route"),

]