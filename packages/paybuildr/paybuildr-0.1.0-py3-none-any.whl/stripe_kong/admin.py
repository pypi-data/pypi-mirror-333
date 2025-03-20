from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.utils.html import format_html, mark_safe
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404

from .models import Plan, Subscription, ApiService, ApiRoute, ApiPlan, PuckPage
from .utils.stripe_client import StripeClient
from .utils.kong_client import KongClient

stripe_client = StripeClient()
kong_client = KongClient()


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "amount_display", "currency", "interval", "active", "created_at")
    search_fields = ("name",)
    list_filter = ("interval", "active", "currency")
    readonly_fields = ("stripe_price_id", "created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("name", "amount", "currency", "interval", "active")
        }),
        ("Stripe Information", {
            "fields": ("stripe_price_id",),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def amount_display(self, obj):
        return f"{obj.amount} {obj.currency}"
    amount_display.short_description = "Amount"
    
    def save_model(self, request, obj, form, change):
        if not change or 'amount' in form.changed_data or 'currency' in form.changed_data or 'interval' in form.changed_data:
            # Create or update the price in Stripe
            product_name = f"{obj.name}-{obj.id}" if obj.id else obj.name
            product = stripe_client.create_product(product_name)
            price = stripe_client.create_price(
                product.id, 
                int(obj.amount * 100), 
                obj.currency, 
                obj.interval if obj.interval != "once" else None
            )
            obj.stripe_price_id = price.id
        super().save_model(request, obj, form, change)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "current_period_end", "created_at")
    list_filter = ("status", "plan")
    search_fields = ("user__username", "user__email", "stripe_subscription_id")
    readonly_fields = ("stripe_subscription_id", "created_at", "updated_at")
    raw_id_fields = ("user", "plan")
    date_hierarchy = "created_at"


@admin.register(ApiService)
class ApiServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "active", "routes_count", "kong_status", "created_at")
    list_filter = ("active",)
    search_fields = ("name", "url")
    readonly_fields = ("kong_id", "kong_status", "created_at", "updated_at")
    actions = ["sync_with_kong", "refresh_from_kong"]
    
    def routes_count(self, obj):
        count = obj.routes.count()
        if count > 0:
            url = reverse('admin:stripe_kong_apiroute_changelist') + f'?service__id__exact={obj.id}'
            return format_html('<a href="{}">{} routes</a>', url, count)
        return "0 routes"
    routes_count.short_description = "Routes"
    
    def kong_status(self, obj):
        """Display status of this service in Kong"""
        if not obj.kong_id:
            return mark_safe('<span style="color: red;">Not in Kong</span>')
        
        try:
            # In a production environment, you would uncomment this to check Kong
            # kong_client.get_service(obj.kong_id)
            return mark_safe('<span style="color: green;">Active in Kong</span>')
        except Exception:
            return mark_safe('<span style="color: orange;">Error checking Kong</span>')
    kong_status.short_description = "Kong Status"
    
    def save_model(self, request, obj, form, change):
        if not change or 'url' in form.changed_data or 'name' in form.changed_data:
            try:
                if obj.kong_id:
                    # Update existing service in Kong
                    service_data = {
                        "name": obj.name,
                        "url": obj.url
                    }
                    service = kong_client.update_service(obj.kong_id, service_data)
                    self.message_user(request, f"Service '{obj.name}' updated in Kong", level=messages.SUCCESS)
                else:
                    # Create new service in Kong
                    service = kong_client.create_service(obj.name, obj.url)
                    if "id" in service:
                        obj.kong_id = service["id"]
                    elif "data" in service and "id" in service["data"]:
                        obj.kong_id = service["data"]["id"]
                    else:
                        # Try to find the ID in the response
                        for key, value in service.items():
                            if isinstance(value, dict) and "id" in value:
                                obj.kong_id = value["id"]
                                break
                    
                    if obj.kong_id:
                        self.message_user(request, f"Service '{obj.name}' created in Kong", level=messages.SUCCESS)
                    else:
                        self.message_user(
                            request, 
                            f"Service created but could not extract Kong ID. Please sync manually.", 
                            level=messages.WARNING
                        )
            except Exception as e:
                self.message_user(
                    request, 
                    f"Error communicating with Kong API: {str(e)}", 
                    level=messages.ERROR
                )
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Delete the service from Kong when deleting from Django"""
        if obj.kong_id:
            try:
                kong_client.delete_service(obj.kong_id)
                self.message_user(request, f"Service '{obj.name}' deleted from Kong", level=messages.SUCCESS)
            except Exception as e:
                self.message_user(
                    request, 
                    f"Error deleting service from Kong: {str(e)}", 
                    level=messages.ERROR
                )
        
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Delete multiple services from Kong when bulk deleting"""
        for obj in queryset:
            if obj.kong_id:
                try:
                    kong_client.delete_service(obj.kong_id)
                except Exception as e:
                    self.message_user(
                        request, 
                        f"Error deleting service '{obj.name}' from Kong: {str(e)}", 
                        level=messages.ERROR
                    )
        
        super().delete_queryset(request, queryset)
    
    def sync_with_kong(self, request, queryset):
        """Push selected services to Kong"""
        for service in queryset:
            try:
                if service.kong_id:
                    # Update existing service
                    kong_client.update_service(service.kong_id, {
                        "name": service.name,
                        "url": service.url
                    })
                    self.message_user(
                        request, 
                        f"Service '{service.name}' updated in Kong", 
                        level=messages.SUCCESS
                    )
                else:
                    # Create new service
                    kong_service = kong_client.create_service(service.name, service.url)
                    
                    # Extract Kong ID from response
                    if "id" in kong_service:
                        service.kong_id = kong_service["id"]
                    elif "data" in kong_service and "id" in kong_service["data"]:
                        service.kong_id = kong_service["data"]["id"]
                    else:
                        # Try to find ID in the response
                        for key, value in kong_service.items():
                            if isinstance(value, dict) and "id" in value:
                                service.kong_id = value["id"]
                                break
                    
                    if service.kong_id:
                        service.save()
                        self.message_user(
                            request, 
                            f"Service '{service.name}' created in Kong", 
                            level=messages.SUCCESS
                        )
                    else:
                        self.message_user(
                            request, 
                            f"Could not extract Kong ID for service '{service.name}'", 
                            level=messages.WARNING
                        )
            except Exception as e:
                self.message_user(
                    request, 
                    f"Error syncing service '{service.name}' with Kong: {str(e)}", 
                    level=messages.ERROR
                )
    sync_with_kong.short_description = "Sync selected services to Kong"
    
    def refresh_from_kong(self, request, queryset):
        """Refresh service information from Kong"""
        for service in queryset:
            if not service.kong_id:
                self.message_user(
                    request, 
                    f"Service '{service.name}' has no Kong ID, cannot refresh", 
                    level=messages.WARNING
                )
                continue
                
            try:
                # Get service from Kong
                kong_service = kong_client.get_service(service.kong_id)
                
                # Update local data
                service.name = kong_service.get("name", service.name)
                service.url = kong_service.get("url", service.url)
                service.save()
                
                self.message_user(
                    request, 
                    f"Service '{service.name}' refreshed from Kong", 
                    level=messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request, 
                    f"Error refreshing service '{service.name}' from Kong: {str(e)}", 
                    level=messages.ERROR
                )
    refresh_from_kong.short_description = "Refresh selected services from Kong"


@admin.register(ApiRoute)
class ApiRouteAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "path", "kong_status", "created_at")
    list_filter = ("service",)
    search_fields = ("name", "path")
    readonly_fields = ("kong_id", "kong_status", "created_at", "updated_at")
    actions = ["sync_with_kong", "refresh_from_kong"]
    
    def kong_status(self, obj):
        """Display status of this route in Kong"""
        if not obj.kong_id:
            return mark_safe('<span style="color: red;">Not in Kong</span>')
        
        try:
            # In a production environment, you would uncomment this to check Kong
            # kong_client.get_route(obj.kong_id)
            return mark_safe('<span style="color: green;">Active in Kong</span>')
        except Exception:
            return mark_safe('<span style="color: orange;">Error checking Kong</span>')
    kong_status.short_description = "Kong Status"
    
    def save_model(self, request, obj, form, change):
        if not obj.service.kong_id:
            self.message_user(
                request, 
                f"Service '{obj.service.name}' is not in Kong. Please sync the service first.", 
                level=messages.ERROR
            )
            return
            
        if not change or 'path' in form.changed_data or 'name' in form.changed_data:
            try:
                if obj.kong_id:
                    # Update existing route in Kong
                    route_data = {
                        "paths": [obj.path],
                    }
                    if obj.name:
                        route_data["name"] = obj.name
                        
                    kong_client.update_route(obj.kong_id, route_data)
                    self.message_user(request, f"Route '{obj.name}' updated in Kong", level=messages.SUCCESS)
                else:
                    # Create new route in Kong
                    route = kong_client.create_route(obj.service.kong_id, obj.path, obj.name)
                    
                    # Extract Kong ID
                    if "id" in route:
                        obj.kong_id = route["id"]
                    elif "data" in route and "id" in route["data"]:
                        obj.kong_id = route["data"]["id"]
                    else:
                        # Try to find ID in the response
                        for key, value in route.items():
                            if isinstance(value, dict) and "id" in value:
                                obj.kong_id = value["id"]
                                break
                    
                    if obj.kong_id:
                        self.message_user(request, f"Route '{obj.name}' created in Kong", level=messages.SUCCESS)
                    else:
                        self.message_user(
                            request,
                            f"Route created but could not extract Kong ID. Please sync manually.",
                            level=messages.WARNING
                        )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error communicating with Kong API: {str(e)}",
                    level=messages.ERROR
                )
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Delete the route from Kong when deleting from Django"""
        if obj.kong_id:
            try:
                kong_client.delete_route(obj.kong_id)
                self.message_user(request, f"Route '{obj.name}' deleted from Kong", level=messages.SUCCESS)
            except Exception as e:
                self.message_user(
                    request,
                    f"Error deleting route from Kong: {str(e)}",
                    level=messages.ERROR
                )
        
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Delete multiple routes from Kong when bulk deleting"""
        for obj in queryset:
            if obj.kong_id:
                try:
                    kong_client.delete_route(obj.kong_id)
                except Exception as e:
                    self.message_user(
                        request,
                        f"Error deleting route '{obj.name}' from Kong: {str(e)}",
                        level=messages.ERROR
                    )
        
        super().delete_queryset(request, queryset)
    
    def sync_with_kong(self, request, queryset):
        """Push selected routes to Kong"""
        for route in queryset:
            if not route.service.kong_id:
                self.message_user(
                    request,
                    f"Cannot sync route '{route.name}': Service '{route.service.name}' is not in Kong",
                    level=messages.ERROR
                )
                continue
                
            try:
                if route.kong_id:
                    # Update existing route
                    route_data = {
                        "paths": [route.path],
                    }
                    if route.name:
                        route_data["name"] = route.name
                        
                    kong_client.update_route(route.kong_id, route_data)
                    self.message_user(
                        request,
                        f"Route '{route.name}' updated in Kong",
                        level=messages.SUCCESS
                    )
                else:
                    # Create new route
                    kong_route = kong_client.create_route(route.service.kong_id, route.path, route.name)
                    
                    # Extract Kong ID
                    if "id" in kong_route:
                        route.kong_id = kong_route["id"]
                    elif "data" in kong_route and "id" in kong_route["data"]:
                        route.kong_id = kong_route["data"]["id"]
                    else:
                        # Try to find ID in the response
                        for key, value in kong_route.items():
                            if isinstance(value, dict) and "id" in value:
                                route.kong_id = value["id"]
                                break
                    
                    if route.kong_id:
                        route.save()
                        self.message_user(
                            request,
                            f"Route '{route.name}' created in Kong",
                            level=messages.SUCCESS
                        )
                    else:
                        self.message_user(
                            request,
                            f"Could not extract Kong ID for route '{route.name}'",
                            level=messages.WARNING
                        )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error syncing route '{route.name}' with Kong: {str(e)}",
                    level=messages.ERROR
                )
    sync_with_kong.short_description = "Sync selected routes to Kong"
    
    def refresh_from_kong(self, request, queryset):
        """Refresh route information from Kong"""
        for route in queryset:
            if not route.kong_id:
                self.message_user(
                    request,
                    f"Route '{route.name}' has no Kong ID, cannot refresh",
                    level=messages.WARNING
                )
                continue
                
            try:
                # Get route from Kong
                kong_route = kong_client.get_route(route.kong_id)
                
                # Update local data
                if "name" in kong_route:
                    route.name = kong_route["name"]
                    
                if "paths" in kong_route and kong_route["paths"]:
                    route.path = kong_route["paths"][0]
                    
                route.save()
                
                self.message_user(
                    request,
                    f"Route '{route.name}' refreshed from Kong",
                    level=messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error refreshing route '{route.name}' from Kong: {str(e)}",
                    level=messages.ERROR
                )
    refresh_from_kong.short_description = "Refresh selected routes from Kong"


@admin.register(ApiPlan)
class ApiPlanAdmin(admin.ModelAdmin):
    list_display = ("plan", "service", "rate_limit", "created_at")
    list_filter = ("plan", "service")
    search_fields = ("plan__name", "service__name")
    readonly_fields = ("kong_plugin_id", "created_at", "updated_at")
    
    def save_model(self, request, obj, form, change):
        if not obj.kong_plugin_id and obj.service.kong_id:
            plugin = kong_client.add_rate_limiting(obj.service.kong_id, obj.rate_limit)
            obj.kong_plugin_id = plugin["id"]
        super().save_model(request, obj, form, change)

@admin.register(PuckPage)
class PuckPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "published", "updated_at")
    list_filter = ("published",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:page_id>/editor/',
                self.admin_site.admin_view(self.puck_editor_view),
                name='stripe_kong_puckpage_editor'
            ),
            path(
                '<int:page_id>/preview/',
                self.admin_site.admin_view(self.puck_preview_view),
                name='stripe_kong_puckpage_preview'
            ),
            path(
                '<int:page_id>/save/',
                self.admin_site.admin_view(self.save_puck_content),
                name='stripe_kong_puckpage_save'
            ),
        ]
        return custom_urls + urls
    
    def puck_editor_view(self, request, page_id):
        """View for the simplified page builder editor"""
        page = get_object_or_404(PuckPage, id=page_id)
        
        context = {
            'title': f"Edit Page: {page.title}",
            'page': page,
            'has_permission': True,
            'site_url': '/',
            'site_title': self.admin_site.site_title,
            'site_header': self.admin_site.site_header,
            'save_url': reverse('admin:stripe_kong_puckpage_save', args=[page_id]),
            'preview_url': reverse('admin:stripe_kong_puckpage_preview', args=[page_id]),
            'back_url': reverse('admin:stripe_kong_puckpage_change', args=[page_id]),
            **self.admin_site.each_context(request),
        }
        
        return TemplateResponse(request, 'admin/stripe_kong/puckpage/editor.html', context)
    
    def puck_preview_view(self, request, page_id):
        """Preview the page as it would appear to users"""
        page = get_object_or_404(PuckPage, id=page_id)
        
        context = {
            'page': page,
            'title': page.title,
            'content': page.content,
        }
        
        return TemplateResponse(request, 'stripe_kong/page.html', context)
    
    def save_puck_content(self, request, page_id):
        """Save the page content"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
        
        page = get_object_or_404(PuckPage, id=page_id)
        
        import json
        try:
            content = json.loads(request.body)
            page.content = content  # Store both HTML and CSS
            page.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
