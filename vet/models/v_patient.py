from django.db import models

class VPatient(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=255)
