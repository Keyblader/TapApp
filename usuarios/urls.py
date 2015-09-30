from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from usuarios import views

urlpatterns = [
    url(r'^list/$', views.usuarios_list),
    url(r'^user/(?P<pk>[0-9]+)/$', views.usuarios_detail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)