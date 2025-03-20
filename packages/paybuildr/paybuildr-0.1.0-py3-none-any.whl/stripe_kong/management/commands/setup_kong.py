from django.core.management.base import BaseCommand
from stripe_kong.models import ApiService, ApiRoute, ApiPlan
from stripe_kong.utils.kong_client import KongClient

class Command(BaseCommand):
    help = "Setup Kong with existing API services, routes and plans"
    
    def handle(self, *args, **options):
        kong_client = KongClient()
        
        services = ApiService.objects.filter(active=True, kong_id__isnull=True)
        self.stdout.write(f"Setting up {services.count()} Kong services...")
        
        for service in services:
            try:
                kong_service = kong_client.create_service(service.name, service.url)
                service.kong_id = kong_service["id"]
                service.save()
                self.stdout.write(self.style.SUCCESS(f"Created service: {service.name}"))
                
                # Create routes for this service
                routes = ApiRoute.objects.filter(service=service, kong_id__isnull=True)
                for route in routes:
                    kong_route = kong_client.create_route(service.kong_id, route.path, route.name)
                    route.kong_id = kong_route["id"]
                    route.save()
                    self.stdout.write(self.style.SUCCESS(f"  Created route: {route.name}"))
                
                # Setup rate limits for this service
                api_plans = ApiPlan.objects.filter(service=service, kong_plugin_id__isnull=True)
                for api_plan in api_plans:
                    plugin = kong_client.add_rate_limiting(service.kong_id, api_plan.rate_limit)
                    api_plan.kong_plugin_id = plugin["id"]
                    api_plan.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Created rate limit: {api_plan.plan.name} - {api_plan.rate_limit}/min"
                        )
                    )
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error setting up {service.name}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS("Kong setup completed"))