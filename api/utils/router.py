from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.reverse import reverse

class CustomRouter(DefaultRouter):
    def __init__(self, *args, custom_routes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_routes = custom_routes or {}

    def get_api_root_view(self, api_urls=None):
        original_view = super().get_api_root_view(api_urls)

        def api_root(request, *args, **kwargs):
            response = original_view(request, *args, **kwargs)
            if isinstance(response, Response):
                for name, route_name in self.custom_routes.items():
                    response.data[name] = reverse(route_name, request=request)
            return response

        return api_root
