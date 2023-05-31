from django.db import models

from vet.models import Race
from vet.models.nourriture import Nourriture


class Attribution(models.Model):
    nourriture=Nourriture.ForeignKey(Nourriture,on_delete=models.CASCADE)
    race=Race.Nourriture.ForeignKey(Race,on_delete=models.CASCADE)
    debut_interval_poids=models.IntegerField()
    fin_interval_poids=models.IntegerField()