from vet.models import Rendez_vous
from vet.models import Patient
from django.shortcuts import render
from vet.models import v_patient
from django.http import HttpResponse
from django.shortcuts import redirect
from vet.models import Tarif_rendez_vous

def nouveau(request):
    patients = v_patient.VPatient.objects.all()
    context = { 'patients' : patients}
    return render(request, 'rendez/Inserer_rendez_vous.html', context)

def Inserer_rendez_vous(request):
    tarif = Tarif_rendez_vous.objects.all()[0]
    client = request.POST.get('client')
    patient = Patient.objects.get(pk=client)
    motif = request.POST.get('motif')
    date_prise = request.POST.get('date_prise')
    date_consultation = request.POST.get('date_consultation')
    duree = request.POST.get('duree')
    rendez_vous = Rendez_vous()
    rendez_vous.date_de_prise = date_prise
    rendez_vous.date_consultation = date_consultation
    rendez_vous.date_fin = date_prise 
    rendez_vous.raison = motif
    rendez_vous.patient = patient
    rendez_vous.etat = 1
    rendez_vous.prix= tarif.valeur * float(duree)
    rendez_vous.temps=1
    rendez_vous.duree=duree
    rendez_vous.save()
    return redirect("/vet/Nouveau_rendez_vous")
    #return response
    


