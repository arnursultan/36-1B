from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.serializers import CustomTokenObtainPairView
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView)

urlpatterns = [
    path("admin/",                    admin.site.urls),
    path("api/token/",                CustomTokenObtainPairView.as_view()),
    path("api/token/refresh/",        TokenRefreshView.as_view()),
    path("api/accounts/",             include("accounts.urls")),

    path(
        "api/schema/", SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/", SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
]
