from django.db import models

class PtDemanda(models.Model):
    id = models.AutoField(primary_key=True)
    altitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField()
    longitude= models.FloatField()

    def __str__(self):
        idPt = 'Demanda '+ str(self.id)
        return idPt

class PtAntena(models.Model):
    id = models.AutoField(primary_key=True)
    altitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField()
    longitude= models.FloatField()

    def __str__(self):
        idPt = 'Antena '+ str(self.id)
        return idPt