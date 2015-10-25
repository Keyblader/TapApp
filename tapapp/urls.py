from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/', include('usuarios.urls', namespace="usuarios")),
    url(r'^tapas/', include('tapas.urls', namespace="tapas")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
