from django.urls import path

from vet.views import rendez_vous_view

urlpatterns = [
    #ce premier path va referencier l'url mysite/ à la vue nommée index
    path("", rendez_vous_view.index, name="index"),
    path("recherche_date_libre", rendez_vous_view.recherche_date_libre, name="recherche_date_libre"),
    path("supprimer_rendez_vous/<int:id_rendez_vous>", rendez_vous_view.supprimer_rendez_vous, name="supprimer__rendez_vous"),
    path("confirmation_suppression/<int:id_rendez_vous>", rendez_vous_view.confirmation_suppression, name="confirmation_suppression"),
    path("rendez_vous_entre_deux_dates", rendez_vous_view.rendez_vous_entre_deux_dates, name="rendez_vous_entre_deux_dates")
]