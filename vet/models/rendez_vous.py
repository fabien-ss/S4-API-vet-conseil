from django.db import models
from datetime import timedelta
from django.db.models import Q
from datetime import datetime
from vet.models import Patient
from django.template.defaultfilters import date as date_filter
from pytz import utc

class Rendez_vous(models.Model):
    date_de_prise=models.DateTimeField()
    date_fin=models.DateTimeField(default=datetime.now())
    date_consultation=models.DateTimeField()
    duree=models.IntegerField(default=1)
    raison=models.CharField(max_length=255)
    temps=models.IntegerField()
    prix=models.FloatField()
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    etat=models.IntegerField(default=0)


    def recherche_date_libre(self, date_debut, date_fin):
        date_occupées = Rendez_vous.objects.filter(
            Q(date_de_prise__gte=date_debut) & Q(date_fin__lte= date_fin)
        )
        return date_occupées
    
    def dates_libres(self, date_debut, date_fin):

        db = date_debut

        date_debut = datetime.fromisoformat(date_debut).replace(tzinfo=utc)
        date_fin = datetime.fromisoformat(date_fin).replace(tzinfo=utc)

        date_occupées = self.recherche_date_libre(date_debut, date_fin)

        donnees_de_test = date_occupées
        dates_libres = []

        for i in range(len(donnees_de_test)):
            
            if donnees_de_test[i].date_de_prise > date_debut:
                constant_date = {
                    'date_de_prise': date_debut,
                    'date_fin': donnees_de_test[i].date_de_prise,
                    'date_consultation': donnees_de_test[i].date_de_prise,
                    'duree': 1,
                    'raison': 'Rendez-vous de test',
                    'temps': 60,
                    'prix': 50.0,
                    'patient': None,
                    'etat': 0
                }
                dates_libres.append(constant_date)
            date_debut = donnees_de_test[i].date_fin
        return date_occupées

    def rendez_vous_à_supprimer(self, id_rendez_vous):
        rendez_vous = Rendez_vous.objects.get(id=id_rendez_vous)
        return rendez_vous

    def tous(self):
        print(Rendez_vous.objects.all())

    def rendez_vous_entre_dates(self, date_debut, date_fin):
        rendez_vous = Rendez_vous.objects.filter(date_de_prise__range=(date_debut, date_fin))
        return rendez_vous    
