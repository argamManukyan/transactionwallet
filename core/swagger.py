from django.urls import path
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Wallet API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


class CustomAutoSchema(SwaggerAutoSchema):
    """Add tags in Swagger auto schema"""

    def get_tags(self, operation_keys=None):
        return (
            self.overrides.get("tags", None)
            or getattr(self.view, "tags", [])
            or [operation_keys[0]]
        )
