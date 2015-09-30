from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from tapas import views

urlpatterns = [
    url(r'^anyadirBar/$', views.anyadirBar),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)