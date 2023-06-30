-- Insertion de 20 rendez-vous
INSERT INTO vet_rendez_vous (date_de_prise, date_consultation, raison, temps, prix, etat, patient_id, date_fin, duree)
VALUES
    (CURRENT_TIMESTAMP, '2023-06-28', 'Raison 1', 30, 100, 1, 1, '2023-06-28 10:30:00', 30),
    (CURRENT_TIMESTAMP, '2023-06-29', 'Raison 2', 45, 150, 1, 2, '2023-06-29 11:15:00', 45),
    -- Ajoutez les 18 autres rendez-vous ici
    (CURRENT_TIMESTAMP, '2023-07-10', 'Raison 20', 60, 200, 1, 1, '2023-07-10 14:00:00', 60);

create or replace view vet_vpatient as
    select p.id, c.nom from vet_patient p join vet_client c
        on p.proprietaire_id = c.id;

drop table vet_tarif_rendez_vous;
create table vet_tarif_rendez_vous(
    id serial primary key,
    date_application timestamp,
    valeur float not null
);

insert into vet_tarif_rendez_vous(date_application, valeur) values(now(), 10000.0);