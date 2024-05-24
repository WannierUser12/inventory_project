from rest_framework.routers import DefaultRouter


class CustomDefaultRouter(DefaultRouter):
    """
    Makes all trailing slashes optional in the URLs used by the viewsets
    Supports base prefix name
    """

    def __init__(self, base_prefix="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_prefix = base_prefix
        self.trailing_slash = "/?"

    def register(self, prefix, viewset, basename=None, **kwargs):
        separator = "/" if prefix else ""
        prefix = f"{self.base_prefix}{separator}{prefix}"
        super().register(prefix, viewset, basename=basename, **kwargs)
