from django.urls import path
from mapa.views import showMap


urlpatterns = [
    path('', showMap, name='showMap-view'),
]