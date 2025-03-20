# apps/api_management/kong_client.py
import requests
from django.conf import settings

class KongClient:
    def __init__(self):
        self.admin_url = settings.KONG_ADMIN_URL
        
    def create_service(self, name, url):
        response = requests.post(f"{self.admin_url}/services/", json={
            "name": name,
            "url": url
        })
        return response.json()
        
    def create_route(self, service_name, paths, name=None):
        response = requests.post(f"{self.admin_url}/services/{service_name}/routes", json={
            "paths": paths if isinstance(paths, list) else [paths],
            "name": name
        })
        return response.json()
        
    def add_rate_limiting(self, service_name, limit_per_minute, consumer=None):
        plugin_data = {
            "name": "rate-limiting",
            "config": {
                "minute": limit_per_minute
            }
        }
        
        if consumer:
            plugin_data["consumer"] = consumer
            
        response = requests.post(
            f"{self.admin_url}/services/{service_name}/plugins", 
            json=plugin_data
        )
        return response.json()