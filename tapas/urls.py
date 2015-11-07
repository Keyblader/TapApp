from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from tapas import views

urlpatterns = [
    url(r'^listaTapas/$', views.TapasList.as_view()),
    url(r'^listaTapasBar/(?P<id_bar>\d+)/$', views.TapasListBar.as_view()),
    url(r'^detalleBar/(?P<id_bar>\d+)/$', views.BarDetail.as_view()),
    url(r'^detalleTapa/(?P<id_tapa>\d+)/$', views.TapaDetail.as_view()),
    url(r'^anyadirBar/$', views.anyadirBar),
    url(r'^anyadirTapa/$', views.anyadirTapa),
    url(r'^anyadirComentario/$', views.anyadirComentario),
    url(r'^anyadirValoracion/(?P<id_tapa>\d+)$', views.anyadirValoracion),
    url(r'^anyadirFoto/$', views.anyadirFoto),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)