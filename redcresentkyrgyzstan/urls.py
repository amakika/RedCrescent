from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger Imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Import AllowAny
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Red Crescent API",
        default_version="v1",
        description="API documentation for the Red Crescent project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="asinarstanbekov51@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),  # Use AllowAny for public access to Swagger
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', include('rest_framework.urls')),  # For login/logout views
    path('api/', include('volonteer.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger and Redoc URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



