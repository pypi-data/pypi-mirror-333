import requests
from django.conf import settings
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class KongClient:
    def __init__(self):
        self.admin_url = settings.KONG_ADMIN_URL
    
    def create_service(self, name, url):
        """
        Create a service in Kong
        
        Returns the parsed JSON response from Kong API
        """
        try:
            # Extract host from URL
            parsed_url = urlparse(url)
            
            # Create service payload
            service_data = {
                "name": name,
                "url": url,
                "host": parsed_url.netloc,
                "protocol": parsed_url.scheme or "http"
            }
            
            # Attempt to create service
            response = requests.post(
                f"{self.admin_url}/services/", 
                json=service_data
            )
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Kong create_service response: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error creating service: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Kong error details: {error_detail}")
                except:
                    logger.error(f"Kong error status: {e.response.status_code}, content: {e.response.content}")
            raise
    
    def get_info(self):
        """
        Get information about the Kong server
        
        Returns the parsed JSON response from Kong API
        """
        try:
            response = requests.get(f"{self.admin_url}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error getting info: {str(e)}")
            raise

    def get_service(self, service_id_or_name):
        """
        Get a service from Kong by ID or name
        
        Returns the parsed JSON response from Kong API
        """
        try:
            response = requests.get(f"{self.admin_url}/services/{service_id_or_name}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error getting service {service_id_or_name}: {str(e)}")
            raise
    
    def get_services(self):
        """
        Get all services from Kong
        
        Returns the parsed JSON response from Kong API with pagination
        """
        try:
            response = requests.get(f"{self.admin_url}/services")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error getting services: {str(e)}")
            raise
    
    def update_service(self, service_id, data):
        """
        Update a service in Kong
        
        Returns the parsed JSON response from Kong API
        """
        try:
            response = requests.patch(f"{self.admin_url}/services/{service_id}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error updating service {service_id}: {str(e)}")
            raise
    
    def delete_service(self, service_id):
        """
        Delete a service from Kong
        
        Returns True if successful
        """
        try:
            response = requests.delete(f"{self.admin_url}/services/{service_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error deleting service {service_id}: {str(e)}")
            raise
    
    def create_route(self, service_id, path, name=None):
        """
        Create a route in Kong linked to a service
        
        Returns the parsed JSON response from Kong API
        """
        route_data = {
            "paths": [path] if isinstance(path, str) else path,
            "service": {"id": service_id}
        }
        
        if name:
            route_data["name"] = name
            
        try:
            response = requests.post(
                f"{self.admin_url}/routes", 
                json=route_data
            )
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Kong create_route response: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error creating route: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Kong error details: {error_detail}")
                except:
                    logger.error(f"Kong error status: {e.response.status_code}, content: {e.response.content}")
            raise
    
    def get_route(self, route_id):
        """
        Get a route from Kong by ID
        
        Returns the parsed JSON response from Kong API
        """
        try:
            response = requests.get(f"{self.admin_url}/routes/{route_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error getting route {route_id}: {str(e)}")
            raise
    
    def get_routes(self, service_id=None):
        """
        Get routes from Kong, optionally filtered by service
        
        Returns the parsed JSON response from Kong API with pagination
        """
        try:
            if service_id:
                response = requests.get(f"{self.admin_url}/services/{service_id}/routes")
            else:
                response = requests.get(f"{self.admin_url}/routes")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error getting routes: {str(e)}")
            raise
    
    def update_route(self, route_id, data):
        """
        Update a route in Kong
        
        Returns the parsed JSON response from Kong API
        """
        try:
            response = requests.patch(f"{self.admin_url}/routes/{route_id}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error updating route {route_id}: {str(e)}")
            raise
    
    def delete_route(self, route_id):
        """
        Delete a route from Kong
        
        Returns True if successful
        """
        try:
            response = requests.delete(f"{self.admin_url}/routes/{route_id}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error deleting route {route_id}: {str(e)}")
            raise
    
    def add_rate_limiting(self, service_id, limit_per_minute, consumer=None):
        """
        Add rate limiting plugin to a service in Kong
        
        Returns the parsed JSON response from Kong API
        """
        plugin_data = {
            "name": "rate-limiting",
            "config": {"minute": limit_per_minute}
        }
        
        if consumer:
            plugin_data["consumer"] = consumer
            
        try:
            response = requests.post(
                f"{self.admin_url}/services/{service_id}/plugins", 
                json=plugin_data
            )
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Kong add_rate_limiting response: {result}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error adding rate limiting: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Kong error details: {error_detail}")
                except:
                    logger.error(f"Kong error status: {e.response.status_code}, content: {e.response.content}")
            raise
    
    def get_plugins(self, service_id=None):
        """
        Get plugins from Kong, optionally filtered by service
        
        Returns the parsed JSON response from Kong API with pagination
        """
        try:
            if service_id:
                response = requests.get(f"{self.admin_url}/services/{service_id}/plugins")
            else:
                response = requests.get(f"{self.admin_url}/plugins")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Kong API error getting plugins: {str(e)}")
            raise