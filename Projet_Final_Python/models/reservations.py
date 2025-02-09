from datetime import datetime , timedelta, date, time
from models.evenements import PlanificationEvenements
from models.salles import GestionnaireSalle
import csv
import os


#Creation de la Classe Reservation
class Reservation:
    """Constructeur de la Classe"""
    def __init__(self, id_reservation, id_salle: str, id_evenement: str):
        self.id_reservation = id_reservation
        self.id_salle = id_salle
        self.id_evenement = id_evenement
        self.date_reservation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

#Creation de la Classe ReservationSalle pour gerer les reservations
class ReservationSalle:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_reservation_csv = os.path.join(base_dir, "..", "data", "gestion_reservations.csv") #path du fichier de sauvegarde des reservations
    path_event_csv = PlanificationEvenements.path_event_csv #path du fichier de sauvegarde des evenements
    path_salle_csv = GestionnaireSalle.path_salle_csv #path du fichier de sauvegarde des salles
    gestion_salle=GestionnaireSalle() #instance de la classe GestionnanireSalle 

    """Constructeur de la Classe ReservationSalle"""
    def __init__(self):
        self.reservations: list[Reservation] = []
        self.load_reservations() 

    """Methode pour charger les reservations depuis le fichier de sauvegarde """
    def load_reservations(self):
        if not os.path.exists(self.path_reservation_csv):
            return
        with open(self.path_reservation_csv, "r") as f: #Ouverture du fichier de sauvegarde
            reader = csv.reader(f)
            next(reader, None)  #Ignorer la premiere ligne du fichier
            for row in reader:
                if row:
                    self.reservations.append(Reservation(row[0], row[1], row[2])) #Ajout des lignes du fichiers a la liste reservations

    """Methode  pour recuperer l'horaire d'une salle avec son id"""
    def get_salle_horaire(self, id_salle: str):
        try:
            with open(self.path_salle_csv, "r") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and row[0] == id_salle:
                        return row[4]  # Horaire au format "HH:MM-HH:MM"
        except FileNotFoundError:
            print(f"Le fichier {self.path_salle_csv} n'existe pas !")
        return None
    
    """Methode pour recupere la Capaciter maximale en terme de personne qu'elle peut recevoir d'une salle"""
    def get_salle_cap_max(self,id_salle: str):
        try:
            with open(self.path_salle_csv, "r") as f: #Ouverture du fichier de sauvegarde
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and row[0] == id_salle: #Verification que c'est bien l"id de la salle voulue
                        return row[2]  # Capaciter maximale de la salle
        
        except FileNotFoundError:
            print(f"Le fichier {self.path_salle_csv} n'existe pas !")
        return None
    
    """Methode pour ajouter une nouvelle reservation"""
    def add_reservation(self, reservation: Reservation):
        salle_horaire = self.get_salle_horaire(reservation.id_salle) #Recuprer l'horaire de la salle a reserver
        event_horaire = self.get_event_date_heure(reservation.id_evenement) #Recuperer L'horaire de l'evenement pour lequel on veut reserver

        for res in self.reservations:
            if res.id_evenement == reservation.id_evenement: #verifie si l'evenement a deja une reservation 
                print(f"Erreur: L'evenement {reservation.id_evenement} a deja une reservation.")
                return False
        if not self.check_event_statut(reservation.id_evenement): return False #Verifie si le statut n'est pas "Annuler" Ou "Terminer"
        
        #Verifie que la Capaciter maximale de la salle est >= au nombre de personne prevu dans l'evenement
        if self.is_cap_max_salle_conflict(reservation.id_salle, reservation.id_evenement)==True:
            print(f"Conflit detecte ! La salle {reservation.id_salle} est deja attribuee a un autre evenement dans le même creneau horaire.")
            print("\n----------------------------------------------------------------Solution alternative----------------------------------------------------------------")
            print("Liste des salles disponible dans ce crenau :\n") #liste des salles Alternative
            avalaible_Salles=self.suggest_alternative_salles( reservation.id_salle,reservation.id_evenement)
            return False

        salle_horaire = self.get_salle_horaire(reservation.id_salle) #Recuprer l'horaire de la salle a reserver
        event_horaire = self.get_event_date_heure(reservation.id_evenement) #Recuperer L'horaire de l'evenement pour lequel on veut reserver
        print("Event horaire---",event_horaire)
        print("Salle Horeire --------",salle_horaire)
        #Verifie qu'il n'ya pas de conflict de salle dans le crenau choisi
        if not self.is_salle_conflict(reservation.id_salle, reservation.id_evenement):
            print(f"Conflit detecte ! La salle {reservation.id_salle} est deja attribuee a un autre evenement dans le même creneau horaire.")
            print("\n----------------------------------------------------------------Solution alternative----------------------------------------------------------------")
            print("Liste des salles disponible dans ce crenau :\n")
            avalaible_Salles=self.suggest_alternative_salles( reservation.id_salle,reservation.id_evenement)
            return False
        
        
        if not salle_horaire or not event_horaire: #Gestion d'erreur, si l'heure de la salle ou de l'evenement manque
            print("Impossible de verifier l'horaire, donnees manquantes.")
            return False
        
        if  not self.check_time_conflict(event_horaire, salle_horaire): #Verifie s'il n'ya pas de conflit dans les differants horaire 
            print(f"Erreur: L'evenement ne correspond pas aux horaires de la salle {reservation.id_salle}.")
            print("\n----------------------------------------------------------------Solution alternative----------------------------------------------------------------")
            print("Liste des salles disponible dans ce crenau :\n")
            avalaible_Salles=self.suggest_alternative_salles( reservation.id_salle,reservation.id_evenement)            
            return False
        

        # Ajouter la reservation
        self.reservations.append(reservation)
        self.save_reservation_changes()
        print("\nRecu de la reservation")
        print(f"Id reservation   : {reservation.id_reservation}")
        print(f"Id Evenement     : {reservation.id_evenement}")
        print(f"Id Salle         : {reservation.id_salle}")
        print(f"Date Reservation : {reservation.date_reservation}\n")
        print("La reservation a ete enregistree avec succès !\n")
        return True

    """Methode qui verifie si le Statut est Annuler ou Terminer"""
    def check_event_statut(self,id_event):
        try:
            with open(self.path_event_csv, "r") as f: #Ouverture du fichier de sauvegarde
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and row[0] == id_event : #verifi que l'id corresond
                        statut = row[5]
                        if statut =="Annuler": #verifie le champs du Statut
                            print("Impossible d'enregistrer cette reservation, cet evenement a ete annuler")
                            return False 
                        elif statut=="Terminer":#verifie le champs du Statut
                            print("Impossible d'enregistrer cette reservation")
                            print("cet evenement a le statut terminer, veuillez creer un autre evenement")
                            return False
                        else: return True #Retourne true si l'evenement n'a pas de statut Annuler ou Terminer
        except FileNotFoundError:
            print(f"Le fichier {self.path_event_csv} n'existe pas !")
    

    """Methode qui verifie le conflit d'eure et empeche que le meme evenemnet ait 2 ou plus reservations"""
    def is_salle_conflict(self, id_salle: str, id_evenement: str) -> bool:
        try:
            with open(self.path_event_csv, "r") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row and row[3] == id_salle and row[0] != id_evenement:  # Verifie que ce n'est pas le meme evenement
                        date_heure_existing = self.get_salle_horaire(id_salle)
                        date_heure_new = self.get_event_date_heure(id_evenement)
                        if date_heure_new and date_heure_existing and self.check_time_conflict(date_heure_new, date_heure_existing):
                        
                            return True
        except FileNotFoundError:
            print(f"Le fichier {self.path_event_csv} n'existe pas !")
        return False

    """Methode pour recupere La date et l'heure d'un evenement"""
    def get_event_date_heure(self, id_event: str):
        try:
            with open(self.path_event_csv, "r") as f:
                reader = csv.reader(f)
                next(reader, None) #ignore l'entete du fichier
                for row in reader:
                    if row and row[0] == id_event: #verifie que l'id correspond 
                        return row[2] #retourne la date et l'heur dans le format YYYY-MM-DD|HH-MM
        except FileNotFoundError:
            print(f"Le fichier {self.path_event_csv} n'existe pas !")
        return None
    
    """Methode pour recuperer le nombre de participant d'un evenement"""
    def get_event_nbre_participant(self, id_event:str):
        try:
            with open(self.path_event_csv, "r") as f: #Ouverture du fichier de sauvegarde
                reader = csv.reader(f)
                next(reader, None) #Ignore l'entete
                for row in reader:
                    if row and row[0] == id_event: #Verifie la correspondance de l'id
                        return row[4] #Retourne le nombre de participant
        except FileNotFoundError:
            print(f"Le fichier {self.path_event_csv} n'existe pas !")
        return None

    """Methode pour verifier qu'il n'y a pas de conflit d'heure entre la salle et l'evenement"""
    def check_time_conflict(self, date_heure_event: str, horaire_salle: str) -> bool:
        try:
            date_event, time_event = date_heure_event.split('|')
            start_event, end_event = map(lambda x: datetime.strptime(x, "%H:%M"), time_event.split('-'))
            start_salle, end_salle = map(lambda x: datetime.strptime(x, "%H:%M"), horaire_salle.split('-'))

            return not (end_event <= start_salle or start_event >= end_salle)  # Conflit s'il y a un chevauchement
        except ValueError as e:
            print(f"Erreur de format d'heure : {e}")
            return False




    def is_cap_max_salle_conflict(self, id_salle:str, id_event: str )->bool:
        cap_max=int(self.get_salle_cap_max(id_salle))
        nbre_max_event = int(self.get_event_nbre_participant(id_event))
        if cap_max and nbre_max_event:
            return cap_max < nbre_max_event
    

  

    def suggest_alternative_salles(self, id_salle_conflictuelle: str, id_evenement: str):
        try:
            event_horaire = self.get_event_date_heure(id_evenement)
            if not event_horaire:
                print(f"Aucun horaire trouve pour l'evenement {id_evenement}.")
                return []

            date_event, time_event = event_horaire.split('|')
            start_event, end_event = map(lambda x: datetime.strptime(x, "%H:%M").time(), time_event.split('-'))

            alternative_salles = []
            with open(self.path_salle_csv, "r") as f:
                reader = csv.reader(f)
                next(reader, None)  # Ignorer l'entete
                for row in reader:
                    if row:
                        id_salle = row[0]
                        salle_horaire = row[4]  # Format HH:MM-HH:MM
                        start_salle, end_salle = map(lambda x: datetime.strptime(x, "%H:%M").time(), salle_horaire.split('-'))

                        # Verifier que la salle n'est pas la salle en conflit et qu'elle est disponible
                        if id_salle != id_salle_conflictuelle and \
                                self.check_time_conflict(event_horaire, salle_horaire) and \
                                not self.is_salle_conflict(id_salle, id_evenement):
                            alternative_salles.append((id_salle, salle_horaire))

            # Afficher les suggestions
            if alternative_salles:
                print("Suggestions de salles alternatives :")
                for salle, horaire in alternative_salles:
                    print(f"salle {salle} disponible de {horaire}")
                return True
            else:
                print("\nAucune salle alternative disponible pour cet evenement.")
                return False

        except FileNotFoundError as e:
            print(f"Fichier manquant : {e}")
            return False



    def show_reservation(self):
        list_res=[]
        try:
            with open(self.path_reservation_csv, "r") as f:
                reader_s=csv.reader(f)
                header = next(reader_s,None)
                list_res=[row for row in reader_s]
                if list_res:
                    print(" | ".join(val.ljust(25) for val in header))
                    print("-" * 140)
                    for row in list_res:
                        print(" | ".join(val.ljust(25) for val in row))
                else:
                    print("Aucune Salle trouvee")
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_reservation_csv} n'existe pas !")

    def show_reservation_by_id(self, id_res:str,compt:int):
        header=["Id Reservation","Id Evenement","Id Salle","Date Reservation"]
        
        res=self.search_reservation_by_id(id_res)
        if res:
            if compt==0:
                print(" | ".join(val.ljust(25) for val in header))
            res_line=res[0]
            print("-" * 140)
            print(" | ".join(val.ljust(25) for val in res_line))
        



    """Methode pour rechercer une reservation avec son id , elle retourne la reservation trouvee"""
    def search_reservation_by_id(self, Id:str):
        res_found=[]
        try:
            with open(self.path_reservation_csv, "r") as f:
                reader_s=csv.reader(f)
                for row in reader_s:
                    if row and row[0].strip()==Id.strip():
                        res_found.append(row)
                        break
            return res_found
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_reservation_csv} n'existe pas !")
    


    def save_reservation_changes(self):
        with open(self.path_reservation_csv, "w", newline="") as f:
            writer = csv.writer(f)
            header = ["Id", "Id_Salle", "Id_Evenement", "Date_reservation"]
            writer.writerow(header)
            for el in self.reservations:
                writer.writerow([el.id_reservation, el.id_salle, el.id_evenement, el.date_reservation])


    def generate_report(self, period: str):
        aujourdhui = date.today()
        reservation_filtre = []

        with open(self.path_reservation_csv,'r') as f:
            reader_r=csv.reader(f)
            header=next(reader_r,None)
            for res in reader_r:
                line_res=[res[0],res[1],res[2], res[3]]
            
                try:
                    date_res = datetime.strptime(res[3], "%Y-%m-%d %H:%M:%S").date()
                except ValueError:
                    date_res = datetime.strptime(res[3], "%Y-%m-%d").date()

                if period == "day" and date_res == aujourdhui:
                    reservation_filtre.append(line_res)

                elif period == "week":
                    debut_semaine = aujourdhui - timedelta(days=aujourdhui.weekday())  # Lundi de la semaine
                    fin_semaine = debut_semaine + timedelta(days=6)  # Dimanche de la semaine
                    if debut_semaine <= date_res <= fin_semaine:
                        reservation_filtre.append(line_res)

                elif period == "month" and date_res.year == aujourdhui.year and date_res.month == aujourdhui.month:
                    reservation_filtre.append(line_res)

        return reservation_filtre

    def show_report(self, reports:list):
        header=["Id Reservation","Id Evenement","Id Salle","Date Reservation"]
        print(" | ".join(val.ljust(25) for val in header))
        print("-"*100)
        for row in reports:
            print(' | '.join(val.ljust(25) for val in row))
