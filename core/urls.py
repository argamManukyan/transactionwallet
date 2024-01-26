from django.contrib import admin
from django.urls import path, include
from core.swagger import swagger_urlpatterns

urlpatterns = [
    path("api/v1/", include("wallet.urls")),
    path("admin/", admin.site.urls),
] + swagger_urlpatterns

