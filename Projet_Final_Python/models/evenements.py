import csv
import os
from utils.fct_utiles import is_header_csv_exist
from models.salles import GestionnaireSalle
from datetime import datetime



class Evenement:

    def __init__(self, id: str, nom: str, date_heure_debut_fin: str, nombre_de_participant: int):
        self.id = id
        self.nom = nom
        self.date_heure_debut_fin = date_heure_debut_fin
        self.id_salle_reserver = None
        self.nombre_de_participant = nombre_de_participant
        self.statut = "En attente"  # Un evenement peut etre en attente, Terminer ou Annuler

    def change_status(self, statut: str):
        self.statut = statut

    def change_salle_reserver(self, id_salle_reserver):
        self.id_salle_reserver = id_salle_reserver  

    def add_Evenement(self, id_salle_reserver):
        self.id_salle_reserver = id_salle_reserver 


class PlanificationEvenements(Evenement):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_event_csv = os.path.join(base_dir, "..", "data", "gestion_evenements.csv")
    path_salle_csv=GestionnaireSalle.path_salle_csv

    def __init__(self):
        self.evenements: list[Evenement] = []

    def add_event(self, evenement):
        self.evenements.append(evenement)

    def show_events_per_salle(self, salle_id: str):
        try:
            list_events = []
            with open(self.path_event_csv, "r") as f:
                reader_e = csv.reader(f)
                header = next(reader_e, None)
                for row in reader_e:
                    if row and row[3].strip() == salle_id:
                        list_events.append(row)

                if list_events:
                    print(" | ".join(val.ljust(25) for val in header))
                    print("-" * 140)
                    for row in list_events:
                        print(" | ".join(val.ljust(25) for val in row))
                else:
                    print(f"Aucun Evenement trouvee ")
                return list_events
        except FileNotFoundError:
            print("Erreur, Fichier non trouver !")


    def show_events_by_id(self, Evenement_id: str):
        try:
            list_events = []
            with open(self.path_event_csv, "r") as f:
                reader_e = csv.reader(f)
                header = next(reader_e, None)
                for row in reader_e:
                    if row and row[0].strip() == Evenement_id:
                        list_events.append(row)

                if list_events:
                    print(" | ".join(val.ljust(25) for val in header))
                    print("-" * 140)
                    for row in list_events:
                        print(" | ".join(val.ljust(25) for val in row))
                else:
                    print(f"Aucun Evenement trouvee ")
                return list_events
        except FileNotFoundError:
            print("Erreur, Fichier non trouver !")

    def show_events(self):
        try:
            list_events = []
            with open(self.path_event_csv, "r") as f:
                reader_e = csv.reader(f)
                header = next(reader_e, None)
                for row in reader_e:
                    list_events.append(row)
                if list_events:
                    print(" | ".join(val.ljust(24) for val in header))
                    print("-" * 120)
                    for row in list_events:
                        print(" | ".join(val.ljust(24) for val in row))
                else:
                    print(f"Aucun Evenement trouvee ")
                return list_events
        except FileNotFoundError:
            print("Erreur, Fichier non trouver !")

    def show_disponibility_salle(self,id_salle :str):
        list_salle_event=[]
        try:
            with open(self.path_salle_csv,'r') as f:
                reader_s=csv.reader(f)
                for row in reader_s:
                    if row[0].split()==id_salle.split():
                        salle_horaire=row[4]

            with open(self.path_event_csv, "r") as f:
                reader_e=csv.reader(f)
                print(f"\nLa salle avec l'Id {id_salle} a pour horaire : (Tout les jours-{salle_horaire})")
                
                for row in reader_e:
                    if row[3].strip()==id_salle.strip():
                        list_salle_event.append(row)
                        date,heure=row[2].split('|')
                        print(f"Elle sera occuper le {date} vers {heure} ")
                if not list_salle_event:
                    print("Elle n'a aucune reservation en cours donc est disponible tout les jours dans son horaire")
                return list_salle_event
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_event_csv} n'existe pas !")


    def edit_evenement(self, Id: str, evenement: Evenement):
        edited_Evenement = [evenement.id, evenement.nom, evenement.date_heure_debut_fin,
                            evenement.id_salle_reserver, evenement.nombre_de_participant, evenement.statut]
        list_Evenement_modified = []

        try:
            with open(self.path_event_csv, "r") as f:
                reader_s = csv.reader(f)
                for row in reader_s:
                    if row and row[0].strip() == Id.strip():
                        list_Evenement_modified.append(edited_Evenement)
                    else:
                        list_Evenement_modified.append(row)

            with open(self.path_event_csv, "w", newline="") as f:
                writer_s = csv.writer(f)
                writer_s.writerows(list_Evenement_modified)

            print(f"L'evenement au No: {Id} a ete mis a jour avec succes")
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_event_csv} n'existe pas !")

    def delete_evenement(self, Id: str):
        list_Evenement_modified = []

        try:
            with open(self.path_event_csv, "r") as f:
                reader_s = csv.reader(f)
                for row in reader_s:
                    if row and row[0] == Id:
                        continue
                    else:
                        list_Evenement_modified.append(row)

            with open(self.path_event_csv, "w", newline="") as f:
                writer_s = csv.writer(f)
                writer_s.writerows(list_Evenement_modified)

            print(f"L'evenement au No: {Id} a ete supprimer avec succes")
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_event_csv} n'existe pas !")

    def search_event_by_id(self, Id: str):
        event_found = []
        try:
            with open(self.path_event_csv, "r") as f:
                reader_s = csv.reader(f)
                for row in reader_s:
                    if row and row[0].strip() == Id.strip():
                        event_found.append(row)
                        break
            return event_found
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_event_csv} n'existe pas !")

    def history_event(self):
        ends_event=[]
        try:
            with open(self.path_event_csv, 'r') as f:
                reader_e=csv.reader(f)
                next(reader_e,None)
                for row in reader_e:
                    if row and row[5].split()=="Terminer".split():
                        ends_event.append(row)
                return ends_event
        except FileNotFoundError:
            print("Fichier gestion_evenements Introuvable")


    def update_events(self):
        try:
            aujourdhui = datetime.now().date() 
            with open(self.path_event_csv,'r') as f:
                reader_e=csv.reader(f)
                for row in reader_e:
                    if row and row[5].strip()=="En attente":
                        date_event, _=row[2].split('|')
                        date_event = datetime.strptime(date_event, "%Y-%m-%d").date()  
                        if aujourdhui>date_event :
                            new_event=Evenement(row[0],row[1],row[2],row[4])
                            new_event.change_salle_reserver(row[3])
                            new_event.change_status("Terminer")
                            self.edit_evenement(row[0], new_event)

        except FileNotFoundError:
            print("Attention le fichier gestion_evenemnt est manquant")



    def save_add_changes(self):
        try:
            with open(self.path_event_csv, "a", newline="") as f:
                writer_s = csv.writer(f)
                header = ["Id", "Nom", "Date_heure_debut_fin", "id_salle_reserver", "Nbre_participant", "Statut"]
                for el in self.evenements:
                    if is_header_csv_exist(self.path_event_csv, header):
                        writer_s.writerow([el.id, el.nom, el.date_heure_debut_fin, el.id_salle_reserver, el.nombre_de_participant, el.statut])
                    else:
                        writer_s.writerow(header)
                        writer_s.writerow([el.id, el.nom, el.date_heure_debut_fin, el.id_salle_reserver, el.nombre_de_participant, el.statut])
                self.evenements=[]
            print("L'evenement a ete enregistrer avec succes !")
        except FileNotFoundError:
            print("Fichier gestion_evenement intreouable ")
