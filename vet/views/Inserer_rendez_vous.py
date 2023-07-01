from vet.models import Rendez_vous
from vet.models import Patient
from django.shortcuts import render
from vet.models import v_patient
from django.http import HttpResponse
from django.shortcuts import redirect
from vet.models import Tarif_rendez_vous
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

def ajouter_a_ces_date(request, date_de_prise, date_fin):
    patients = v_patient.VPatient.objects.all()
    context = { 'patients' : patients, "date_de_prise" : date_de_prise }
    return render(request, 'rendez/Inserer_rendez_vous.html', context)

def nouveau(request):
    patients = v_patient.VPatient.objects.all()
    context = { 'patients' : patients}
    return render(request, 'rendez/Inserer_rendez_vous.html', context)

def Inserer_rendez_vous(request):

    tarif = Tarif_rendez_vous.objects.latest('id')
    client = request.POST.get('client')
    patient = Patient.objects.get(pk=client)
    motif = request.POST.get('raison')
    date_prise = request.POST.get('date_prise')
    date_consultation = request.POST.get('date_consultation')
    duree = request.POST.get('duree')
    rendez_vous = Rendez_vous()

    date_prise = datetime.fromisoformat(date_prise)
    date_consultation = datetime.fromisoformat(date_consultation)

    rendez_vous.date_de_prise = date_prise

    rendez_vous.date_fin = date_prise + timedelta(hours=int(duree))

    rendez_vous.date_consultation = date_consultation

    rendez_vous.raison = motif
    rendez_vous.patient = patient
    rendez_vous.etat = 1
    rendez_vous.prix= tarif.valeur * float(duree)
    rendez_vous.temps=1
    rendez_vous.duree=duree
    try:
        rendez_vous.check_date()
    except ValidationError as e:
       
        error_messages = e.message
        patients = v_patient.VPatient.objects.all()
        context = { 'patients' : patients, "error" : error_messages}
        return render(request, 'rendez/Inserer_rendez_vous.html', context)
    return redirect("/vet/Nouveau_rendez_vous")
    
    


