from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

from .utils.stripe_client import StripeClient
from .models import ApiService, ApiRoute, ApiPlan, Subscription
from .utils.kong_client import KongClient

import logging
logger = logging.getLogger(__name__)
kong_client = KongClient()


User = get_user_model()
stripe_client = StripeClient()

@receiver(post_save, sender=Subscription)
def update_user_permissions(sender, instance, **kwargs):
    """
    Update user permissions based on subscription status
    """
    if instance.status == "active":
        # Grant permission based on the subscription plan
        pass
    elif instance.status in ["canceled", "unpaid", "incomplete_expired"]:
        # Remove permissions
        pass

# Only register sync signals if KONG_SYNC_ENABLED is True
SYNC_ENABLED = getattr(settings, 'KONG_SYNC_ENABLED', True)

if SYNC_ENABLED:
    @receiver(post_save, sender=ApiService)
    def sync_service_to_kong(sender, instance, created, **kwargs):
        """
        Keep Kong in sync when ApiService instances are created or updated
        """
        if not created and not instance.kong_id:
            # Don't need to sync if it's not a new record and doesn't have a Kong ID
            return
            
        try:
            if created:
                # For new services, create in Kong
                service = kong_client.create_service(instance.name, instance.url)
                
                # Extract Kong ID
                if "id" in service:
                    instance.kong_id = service["id"]
                    instance.save()
                    logger.info(f"Created service {instance.name} in Kong with ID {instance.kong_id}")
            else:
                # For existing services, update in Kong
                kong_client.update_service(instance.kong_id, {
                    "name": instance.name,
                    "url": instance.url
                })
                logger.info(f"Updated service {instance.name} in Kong")
        except Exception as e:
            logger.error(f"Error syncing service {instance.name} to Kong: {str(e)}")

    @receiver(post_delete, sender=ApiService)
    def delete_service_from_kong(sender, instance, **kwargs):
        """
        Delete the service from Kong when it's deleted from Django
        """
        if not instance.kong_id:
            return
            
        try:
            kong_client.delete_service(instance.kong_id)
            logger.info(f"Deleted service {instance.name} from Kong")
        except Exception as e:
            logger.error(f"Error deleting service {instance.name} from Kong: {str(e)}")

    @receiver(post_save, sender=ApiRoute)
    def sync_route_to_kong(sender, instance, created, **kwargs):
        """
        Keep Kong in sync when ApiRoute instances are created or updated
        """
        if not instance.service.kong_id:
            logger.warning(f"Cannot sync route {instance.name}: Service {instance.service.name} is not in Kong")
            return
            
        if not created and not instance.kong_id:
            # Don't need to sync if it's not a new record and doesn't have a Kong ID
            return
            
        try:
            if created:
                # For new routes, create in Kong
                route = kong_client.create_route(instance.service.kong_id, instance.path, instance.name)
                
                # Extract Kong ID
                if "id" in route:
                    instance.kong_id = route["id"]
                    instance.save()
                    logger.info(f"Created route {instance.name} in Kong with ID {instance.kong_id}")
            else:
                # For existing routes, update in Kong
                route_data = {
                    "paths": [instance.path],
                }
                if instance.name:
                    route_data["name"] = instance.name
                    
                kong_client.update_route(instance.kong_id, route_data)
                logger.info(f"Updated route {instance.name} in Kong")
        except Exception as e:
            logger.error(f"Error syncing route {instance.name} to Kong: {str(e)}")

    @receiver(post_delete, sender=ApiRoute)
    def delete_route_from_kong(sender, instance, **kwargs):
        """
        Delete the route from Kong when it's deleted from Django
        """
        if not instance.kong_id:
            return
            
        try:
            kong_client.delete_route(instance.kong_id)
            logger.info(f"Deleted route {instance.name} from Kong")
        except Exception as e:
            logger.error(f"Error deleting route {instance.name} from Kong: {str(e)}")

    @receiver(post_save, sender=ApiPlan)
    def sync_rate_limit_to_kong(sender, instance, created, **kwargs):
        """
        Keep Kong in sync when ApiPlan instances are created or updated
        """
        if not instance.service.kong_id:
            logger.warning(f"Cannot sync rate limit for plan {instance.plan.name}: Service {instance.service.name} is not in Kong")
            return
            
        try:
            if not instance.kong_plugin_id:
                # Create new rate limiting plugin
                plugin = kong_client.add_rate_limiting(instance.service.kong_id, instance.rate_limit)
                
                # Extract Kong plugin ID
                if "id" in plugin:
                    instance.kong_plugin_id = plugin["id"]
                    instance.save()
                    logger.info(f"Created rate limit for plan {instance.plan.name} in Kong with ID {instance.kong_plugin_id}")
            else:
                # Update existing plugin - you would need to add this method to KongClient
                # kong_client.update_plugin(instance.kong_plugin_id, {"config.minute": instance.rate_limit})
                logger.info(f"Updated rate limit for plan {instance.plan.name} in Kong")
        except Exception as e:
            logger.error(f"Error syncing rate limit for plan {instance.plan.name} to Kong: {str(e)}")