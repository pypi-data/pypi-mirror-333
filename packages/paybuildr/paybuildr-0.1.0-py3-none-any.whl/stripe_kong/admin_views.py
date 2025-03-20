from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import ApiService, ApiRoute, ApiPlan
from .utils.kong_client import KongClient

@staff_member_required
def kong_status(request):
    """Admin view for Kong API Gateway status"""
    kong_client = KongClient()
    kong_admin_url = settings.KONG_ADMIN_URL
    sync_enabled = getattr(settings, 'KONG_SYNC_ENABLED', True)
    is_connected = False
    kong_version = ""
    services_count = 0
    routes_count = 0
    plugins_count = 0
    error_message = ""
    
    # Check connection to Kong
    try:
        # Get Kong information
        kong_info = kong_client.get_info()
        is_connected = True
        kong_version = kong_info.get('version', 'Unknown')
        
        # Get services count
        services_response = kong_client.get_services()
        services_count = len(services_response.get('data', []))
        
        # Get routes count
        routes_response = kong_client.get_routes()
        routes_count = len(routes_response.get('data', []))
        
        # Get plugins count
        plugins_response = kong_client.get_plugins()
        plugins_count = len(plugins_response.get('data', []))
    except Exception as e:
        is_connected = False
        error_message = str(e)
    
    # Get unsynchronized items
    unsync_services = ApiService.objects.filter(kong_id__isnull=True)
    unsync_routes = ApiRoute.objects.filter(kong_id__isnull=True)
    
    # Handle POST requests for sync actions
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'sync_all':
            # Sync all services and routes to Kong
            services_synced = 0
            routes_synced = 0
            
            # First sync all services
            for service in unsync_services:
                try:
                    kong_service = kong_client.create_service(service.name, service.url)
                    
                    # Extract Kong ID
                    if "id" in kong_service:
                        service.kong_id = kong_service["id"]
                        service.save()
                        services_synced += 1
                except Exception as e:
                    messages.error(request, _(f"Error syncing service '{service.name}': {str(e)}"))
            
            # Then sync all routes with services that have Kong IDs
            synced_service_ids = [s.id for s in ApiService.objects.filter(kong_id__isnull=False)]
            routes_to_sync = ApiRoute.objects.filter(
                kong_id__isnull=True, 
                service__id__in=synced_service_ids
            )
            
            for route in routes_to_sync:
                try:
                    kong_route = kong_client.create_route(route.service.kong_id, route.path, route.name)
                    
                    # Extract Kong ID
                    if "id" in kong_route:
                        route.kong_id = kong_route["id"]
                        route.save()
                        routes_synced += 1
                except Exception as e:
                    messages.error(request, _(f"Error syncing route '{route.name}': {str(e)}"))
            
            if services_synced > 0 or routes_synced > 0:
                messages.success(
                    request, 
                    _(f"Successfully synced {services_synced} services and {routes_synced} routes to Kong.")
                )
            else:
                messages.info(request, _("No items needed synchronization."))
                
            return redirect(request.path)
            
        elif action == 'refresh_all':
            # Refresh all Kong data into Django
            from django.core.management import call_command
            
            try:
                # Call the sync_from_kong management command
                call_command('sync_from_kong', force=True)
                messages.success(request, _("Successfully refreshed all data from Kong."))
            except Exception as e:
                messages.error(request, _(f"Error refreshing data from Kong: {str(e)}"))
                
            return redirect(request.path)
    
    # Prepare context
    context = {
        'title': _('Kong API Gateway Status'),
        'kong_admin_url': kong_admin_url,
        'is_connected': is_connected,
        'kong_version': kong_version,
        'services_count': services_count,
        'routes_count': routes_count,
        'plugins_count': plugins_count,
        'error_message': error_message,
        'sync_enabled': sync_enabled,
        'unsync_services': unsync_services,
        'unsync_routes': unsync_routes,
    }
    
    return render(request, 'admin/stripe_kong/kong_status.html', context)

@staff_member_required
def sync_api_service(request, service_id):
    """Admin view to sync a specific API Service with Kong"""
    service = ApiService.objects.get(pk=service_id)
    kong_client = KongClient()
    
    try:
        if service.kong_id:
            # Update existing service
            kong_client.update_service(service.kong_id, {
                "name": service.name,
                "url": service.url
            })
            messages.success(request, _(f"Service '{service.name}' updated in Kong"))
        else:
            # Create new service
            kong_service = kong_client.create_service(service.name, service.url)
            
            # Extract Kong ID
            if "id" in kong_service:
                service.kong_id = kong_service["id"]
                service.save()
                messages.success(request, _(f"Service '{service.name}' created in Kong"))
            else:
                messages.warning(request, _(f"Could not extract Kong ID for service '{service.name}'"))
    except Exception as e:
        messages.error(request, _(f"Error syncing service with Kong: {str(e)}"))
    
    return redirect('admin:stripe_kong_apiservice_changelist')

@staff_member_required
def sync_api_route(request, route_id):
    """Admin view to sync a specific API Route with Kong"""
    route = ApiRoute.objects.get(pk=route_id)
    kong_client = KongClient()
    
    if not route.service.kong_id:
        messages.error(
            request, 
            _(f"Service '{route.service.name}' is not in Kong. Please sync the service first.")
        )
        return redirect('admin:stripe_kong_apiroute_changelist')
    
    try:
        if route.kong_id:
            # Update existing route
            kong_client.update_route(route.kong_id, {
                "paths": [route.path],
                "name": route.name
            })
            messages.success(request, _(f"Route '{route.name}' updated in Kong"))
        else:
            # Create new route
            kong_route = kong_client.create_route(route.service.kong_id, route.path, route.name)
            
            # Extract Kong ID
            if "id" in kong_route:
                route.kong_id = kong_route["id"]
                route.save()
                messages.success(request, _(f"Route '{route.name}' created in Kong"))
            else:
                messages.warning(request, _(f"Could not extract Kong ID for route '{route.name}'"))
    except Exception as e:
        messages.error(request, _(f"Error syncing route with Kong: {str(e)}"))
    
    return redirect('admin:stripe_kong_apiroute_changelist')