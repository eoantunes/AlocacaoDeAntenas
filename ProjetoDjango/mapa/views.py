from django.shortcuts import render, get_object_or_404
from mapa.models import PtAntena, PtDemanda
import folium

brasil = folium.Map(
    tiles='Stamen Terrain',
    location=[-15.796401, -47.874189],
    zoom_start=14
)
brasil.add_child(folium.ClickForMarker(popup='PtDemanda'))
brasil = brasil._repr_html_()

def showMap(request):
    obj = get_object_or_404(PtDemanda, id=1)

    context = {
        'map': brasil,
    }

    return render(request, 'index.html', context)