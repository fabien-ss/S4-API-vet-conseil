from datetime import datetime, timedelta

from django.db import models
from pytz import utc
from vet.models import Patient


class Rendez_vous(models.Model):
    date_de_prise=models.DateTimeField()
    date_fin=models.DateTimeField()
    date_consultation=models.DateTimeField()
    duree=models.IntegerField(default=1)
    raison=models.CharField(max_length=255)
    temps=models.IntegerField()
    prix=models.FloatField()
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    etat=models.IntegerField(default=0)

    def recherche_date_libre(self, date_debut, date_fin):
        date_occupées = Rendez_vous.objects.filter(
            date_de_prise__range=(date_debut, date_fin)
        )
        return date_occupées
    
    def dates_libres(self, date_debut, date_fin):
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
                }
                dates_libres.append(constant_date)
            date_debut = donnees_de_test[i].date_fin
        derniere_date = {
            'date_de_prise': date_debut,
            'date_fin': date_fin,
        }
        if(len(date_occupées) > 0):
            derniere_date = {
                'date_de_prise': date_occupées[len(date_occupées) - 1].date_fin,
                'date_fin': date_fin,
            }
        dates_libres.append(derniere_date)
        
        return dates_libres

    def rendez_vous_à_supprimer(self, id_rendez_vous):
        rendez_vous = Rendez_vous.objects.get(id=id_rendez_vous)
        return rendez_vous

    def tous(self):
        print(Rendez_vous.objects.all())

    def rendez_vous_entre_dates(self, date_debut, date_fin):
        rendez_vous = Rendez_vous.objects.filter(date_de_prise__range=(date_debut, date_fin))
        return rendez_vous    

    def get_all_rendezvous(self):
        return Rendez_vous.objects.all()
    
    def get_all_rendez_vous_by_date(self, date):
        return Rendez_vous.objects.filter(date_de_prise__date=date)

    def rendez_vous_entre_2_dates(self, date_debut, date_fin):
        return Rendez_vous.objects.filter(date_de_prise__range=(date_debut, date_fin))
