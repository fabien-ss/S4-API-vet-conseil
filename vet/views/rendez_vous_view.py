from django.http import HttpResponse
from django.shortcuts import render, redirect
from vet.models import formulaire_recherche_date_libre
from vet.models import Rendez_vous
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    return render(request, "rendez_vous/affichage_date_libre.html")

def recherche_date_libre(request):
    if request.method == "POST":
        rendez_vous = Rendez_vous()
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        date_occupées = rendez_vous.dates_libres(date_debut, date_fin)
        return render(request, "rendez_vous/affichage_date_libre.html", { 'date_occupées': date_occupées, 'date_fin' : date_fin, 'date_debut' : date_debut})    
    return render(request, "rendez_vous/affichage_date_libre.html")

def supprimer_rendez_vous(request, id_rendez_vous):
    rendez_vous = Rendez_vous()
    rendez_vous = rendez_vous.rendez_vous_à_supprimer(id_rendez_vous)
    return render(request, "rendez_vous/supprimer_rendez_vous", { "rendez_vous" : rendez_vous})

def confirmation_suppression(request, id_rendez_vous):
    rendez_vous = Rendez_vous()
    rendez_vous = rendez_vous.rendez_vous_à_supprimer(id_rendez_vous)
    rendez_vous.delete()
    return redirect("/vet/")

def rendez_vous_entre_deux_dates(request):
    date_debut = request.POST.get("date_debut")
    date_fin = request.POST.get("date_fin")
    rendez_vous = Rendez_vous.rendez_vous_entre_dates(date_debut, date_fin)
    return render(request, "rendez_vous/affichage_date_libre.html", { 'rendez_vous': rendez_vous })