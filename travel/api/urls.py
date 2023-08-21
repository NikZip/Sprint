from django.urls import path
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Документация к API для приложения для перевалов",
        default_version='v1',
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('perivals', PassCreateApiView.as_view(), name='passes_add'),
    path('perivals/<int:pk>', PassDetailApiView.as_view(), name='pass_detail'),
    path('perivals/search/', PassListQueryView.as_view(), name='pass_query'),
]