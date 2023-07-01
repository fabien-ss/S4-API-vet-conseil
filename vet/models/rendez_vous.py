from datetime import datetime, timedelta, time

from django.db import models
from pytz import utc
from vet.models import Patient, Personnel
from django.utils import timezone

from django.core.exceptions import ValidationError

def validate_positive_integer(value):
    if value <= 0:
        raise ValidationError("La valeur doit être un entier positif.")

def validate_positive_float(value):
    if value <= 0:
        raise ValidationError("La valeur doit être un nombre à virgule positive.")

class Rendez_vous(models.Model):
    date_de_prise = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(default=timezone.now)
    date_consultation = models.DateTimeField(default=timezone.now)
    duree = models.IntegerField(default=1, validators=[validate_positive_integer])
    raison = models.CharField(max_length=700)
    temps = models.IntegerField(default=0, validators=[validate_positive_integer])
    prix = models.FloatField(validators=[validate_positive_float])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    etat = models.IntegerField(default=0, validators=[validate_positive_integer])
    #personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, default=1)

    def clean(self):
        if self.raison == "":
            raise ValidationError("Raison vide")
        
        if int(self.duree)   <= 0:
            raise ValidationError("La durée doit-être strictement positive")

        if self.date_consultation >= self.date_de_prise:
            raise ValidationError("La date de consultation doit être antérieure à la date de prise.")
        
        if self.date_de_prise >= self.date_fin:
            raise ValidationError("La date de prise doit être antérieure à la date de fin.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Rendez_vous, self).save(*args, **kwargs)

    def recherche_date_libre(self, date_debut, date_fin):
        date_occupées = Rendez_vous.objects.filter(
            date_de_prise__range=(date_debut, date_fin), etat = 0
        )
        return date_occupées
    
    def dates_libres(self, date_debut, date_fin):
        
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

        
        nouvelles_dates = []
        
        for date in dates_libres:
            if(date['date_de_prise'].date() < date['date_fin'].date()):
                print("ecart jour")
                print(date['date_de_prise'].date())
                print(date['date_fin'].date())
                while date['date_de_prise'] < date['date_fin']:
                    date_ = date['date_de_prise']
                    new_date = {}
                    if date_.time() < time(8, 0):
                        new_date = {
                            'date_de_prise': date_.replace(hour=8, minute=0, second=0),
                            'date_fin': date_.replace(hour=15, minute=0, second=0)
                        }
                    else:
                        new_date = {
                            'date_de_prise': date_,
                            'date_fin': date_.replace(hour=15, minute=0, second=0)
                        }
                    nouvelles_dates.append(new_date)
                    date['date_de_prise'] += timedelta(days=1)
            else:
                nouvelles_dates.append(date) 
        return dates_libres

    def rendez_vous_à_supprimer(self, id_rendez_vous):
        rendez_vous = Rendez_vous.objects.get(id=id_rendez_vous)
        return rendez_vous

    def rendez_vous_entre_dates(self, date_debut, date_fin):
        rendez_vous = Rendez_vous.objects.filter(date_de_prise__range=(date_debut, date_fin), etat = 0)
        return rendez_vous    

    def get_all_rendezvous(self):
        return Rendez_vous.objects.filter(etat = 0)
    
    def get_all_rendez_vous_by_date(self, date):
        return Rendez_vous.objects.filter(date_de_prise__date=date, etat = 0)

    def rendez_vous_entre_2_dates(self, date_debut, date_fin):
        return Rendez_vous.objects.filter(date_de_prise__range=(date_debut, date_fin), etat = 0)

    def check_date(self):

        all_rendezvous_dates = Rendez_vous.objects.filter(
            Q(date_de_prise__range=(self.date_de_prise, self.date_fin)) |
            Q(date_fin__range=(self.date_de_prise, self.date_fin)),
            Q(etat = 0)
        )

        if all_rendezvous_dates.exists():
            raise ValidationError("Date déjà occupée")
        self.save()