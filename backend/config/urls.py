from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'HMS API'})


urlpatterns = [
    path('admin/', admin.site.urls),

    # Health check
    path('health/', health_check, name='health_check'),

    # API schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

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
