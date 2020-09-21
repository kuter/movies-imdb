"""movies-imdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework import routers

from movies import views as movies_views
from comments import views as comments_views

router = routers.DefaultRouter()

router.register(r'movies', movies_views.MovieViewSet, basename='movie')
router.register(r'comments', comments_views.CommentViewSet, basename='comment')
router.register(r'top', comments_views.TopCommentViewSet, basename='top')

schema_view = get_schema_view(
    openapi.Info(
        title="Movies API",
        default_version='v1',
        # description="Test API",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@devktr.pl"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    re_path('^swagger(?P<format>|\\.json\\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
]
