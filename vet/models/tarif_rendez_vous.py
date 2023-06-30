from django.db import models

class Tarif_rendez_vous(models.Model):
    date_application = models.DateTimeField()
    valeur = models.FloatField()