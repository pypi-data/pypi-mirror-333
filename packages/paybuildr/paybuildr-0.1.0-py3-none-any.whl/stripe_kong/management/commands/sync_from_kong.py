# stripe_kong/management/commands/sync_from_kong.py
from django.core.management.base import BaseCommand
from stripe_kong.models import ApiService, ApiRoute
from stripe_kong.utils.kong_client import KongClient
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Sync API services and routes from Kong to Django database"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Override existing Django records with Kong data',
        )
    
    def handle(self, *args, **options):
        force = options.get('force', False)
        kong_client = KongClient()
        self.stdout.write("Starting Kong synchronization...")
        
        # Sync services
        try:
            services_response = kong_client.get_services()
            services = services_response.get('data', [])
            self.stdout.write(f"Found {len(services)} services in Kong")
            
            for service in services:
                kong_id = service.get('id')
                name = service.get('name')
                url = service.get('url')
                
                if not (kong_id and name and url):
                    self.stdout.write(self.style.WARNING(f"Skipping incomplete service: {service}"))
                    continue
                
                # Try to find existing service by kong_id
                service_obj = ApiService.objects.filter(kong_id=kong_id).first()
                
                # If not found by kong_id, try by name
                if not service_obj:
                    service_obj = ApiService.objects.filter(name=name).first()
                
                if service_obj:
                    if force:
                        # Update the existing record
                        service_obj.name = name
                        service_obj.url = url
                        service_obj.kong_id = kong_id
                        service_obj.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated service: {name}"))
                    else:
                        # Skip if not forcing update
                        self.stdout.write(f"Service exists: {name} (use --force to update)")
                else:
                    # Create new record
                    ApiService.objects.create(
                        name=name,
                        url=url,
                        kong_id=kong_id,
                        active=True
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created service: {name}"))
                
                # Sync routes for this service
                self._sync_routes(kong_client, kong_id, force)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error syncing services: {str(e)}"))
            logger.exception("Error during Kong sync")
        
        self.stdout.write(self.style.SUCCESS("Kong synchronization completed"))
    
    def _sync_routes(self, kong_client, service_id, force):
        try:
            routes_response = kong_client.get_routes(service_id)
            routes = routes_response.get('data', [])
            self.stdout.write(f"Found {len(routes)} routes for service {service_id}")
            
            service_obj = ApiService.objects.filter(kong_id=service_id).first()
            if not service_obj:
                self.stdout.write(self.style.WARNING(f"Cannot sync routes: service {service_id} not found"))
                return
            
            for route in routes:
                kong_id = route.get('id')
                name = route.get('name', f"route-{kong_id[:8]}")  # Create a name if none exists
                paths = route.get('paths', [])
                
                if not (kong_id and paths):
                    self.stdout.write(self.style.WARNING(f"Skipping incomplete route: {route}"))
                    continue
                
                # Use the first path for the path field
                path = paths[0] if paths else ""
                
                # Try to find existing route by kong_id
                route_obj = ApiRoute.objects.filter(kong_id=kong_id).first()
                
                if route_obj:
                    if force:
                        # Update the existing record
                        route_obj.name = name
                        route_obj.path = path
                        route_obj.service = service_obj
                        route_obj.save()
                        self.stdout.write(self.style.SUCCESS(f"  Updated route: {name}"))
                    else:
                        # Skip if not forcing update
                        self.stdout.write(f"  Route exists: {name} (use --force to update)")
                else:
                    # Create new record
                    ApiRoute.objects.create(
                        name=name,
                        path=path,
                        service=service_obj,
                        kong_id=kong_id
                    )
                    self.stdout.write(self.style.SUCCESS(f"  Created route: {name}"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error syncing routes for service {service_id}: {str(e)}"))
            logger.exception(f"Error syncing routes for service {service_id}")