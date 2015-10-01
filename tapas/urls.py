from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from tapas import views

urlpatterns = [
    url(r'^anyadirBar/$', views.anyadirBar),
    url(r'^anyadirTapa/$', views.anyadirTapa),
    url(r'^anyadirComentario/$', views.anyadirComentario),
    url(r'^anyadirValoracion/$', views.anyadirValoracion),
    url(r'^anyadirFoto/$', views.anyadirFoto),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)