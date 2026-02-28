from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'HMS API'})


# drf-yasg schema view
yasg_schema_view = get_schema_view(
    openapi.Info(
        title='Hospital Management System API',
        default_version='v1',
        description=(
            'Comprehensive REST API for the HMS covering patients, ADT, '
            'appointments, clinical, nursing, pharmacy, inventory, '
            'laboratory, and billing modules.'
        ),
        contact=openapi.Contact(email='admin@hms.local'),
        license=openapi.License(name='Proprietary'),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health check
    path('health/', health_check, name='health_check'),

    # drf-spectacular (OpenAPI 3)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # drf-yasg (OpenAPI 2 / Swagger 2.0)
    re_path(
        r'^api/yasg/swagger(?P<format>\.json|\.yaml)$',
        yasg_schema_view.without_ui(cache_timeout=0),
        name='yasg-schema-json',
    ),
    path(
        'api/yasg/swagger/',
        yasg_schema_view.with_ui('swagger', cache_timeout=0),
        name='yasg-swagger-ui',
    ),
    path(
        'api/yasg/redoc/',
        yasg_schema_view.with_ui('redoc', cache_timeout=0),
        name='yasg-redoc',
    ),

    # API v1
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/accounts/', include('apps.accounts.urls_accounts')),
    path('api/v1/patients/', include('apps.patients.urls')),
    path('api/v1/adt/', include('apps.adt.urls')),
    path('api/v1/appointments/', include('apps.appointments.urls')),
    path('api/v1/clinical/', include('apps.clinical.urls')),
    path('api/v1/nursing/', include('apps.nursing.urls')),
    path('api/v1/pharmacy/', include('apps.pharmacy.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/laboratory/', include('apps.laboratory.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
]
