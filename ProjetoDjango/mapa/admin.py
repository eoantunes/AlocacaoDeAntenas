from django.contrib import admin
from mapa.models import PtDemanda, PtAntena

class PtDemandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'altitude')

class PtAntenaAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'altitude')

admin.site.register(PtDemanda, PtDemandaAdmin)
admin.site.register(PtAntena, PtAntenaAdmin)

