import csv
from utils.fct_utiles import is_header_csv_exist
import os

#Creation de la classe salle 
class Salle:
    """COnstructeur de la classe salle"""
    def __init__(self, id:str ,nom :str, capacite_max :int, equipements, horaire:str):
        self.id=id
        self.nom=nom
        self.capacite_max=capacite_max
        self.equipements=equipements 
        self.horaire=horaire
    

    """Methode pour ajouter une liste d'equipement a la classe salle"""
    def add_equipement(self,equipements:list):
        self.equipements=list[equipements]
        
    """Methode string overwrite de la classe salle"""
    def __str__(self)->str:
        return f"Id: {self.id} \nNom : {self.nom} \nCapacite maximum : {self.capacite_max} personnes \nEquipement : {','.join(str(el) for el in self.equipements)} \nHoraire : {self.horaire} "
        
    #Creation de la classe Gestionnairesalle  
class GestionnaireSalle:
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    #Variale de classe qui recoit le chemin vers le fichier gestion_salles.csv
    path_salle_csv = os.path.join(base_dir,"..", "data", "gestion_salles.csv") 


    """Constructeur de la classe GestionnaireSalle"""
    def __init__(self):
        self.salles : list[Salle]=[]
        
    """Methode permettans une liste de """
    def add_salle(self, salle:Salle):
        self.salles.append(salle)


    """Methode pour modifier une salle avec son id dans le fichier csv"""
    def edit_salle(self, Id:str,salle:Salle):
        edited_salle = [salle.id, salle.nom, salle.capacite_max, salle.equipements, salle.horaire]
        list_salle_modified=[]
        try:
            with open(self.path_salle_csv, "r") as f:# Ouverture du ficier de sauvegarde
                reader_s=csv.reader(f)
                for row in reader_s:
                    if row and row[0].strip()==Id.strip():
                        list_salle_modified.append(edited_salle) # ajout de la salle modifier la la place de l'ancienne
                    else:
                        list_salle_modified.append(row)
            with open(self.path_salle_csv,"w",newline="") as f:
                writer_s=csv.writer(f)
                writer_s.writerows(list_salle_modified) #enregistrement de toutes les salles dans le fichier csv
            print(f"La Salle No: {Id} a ete modifier avec succes")
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_salle_csv} n'existe pas !")

    """Methode pour supprimer une salle avec son Id dans le fichier csv"""
    def delete_salle(self, Id:str):
        list_salle_modified=[]
        try:
            with open(self.path_salle_csv, "r") as f:#Ouverture du ficier de sauvegarde
                reader_s=csv.reader(f)
                for row in reader_s:
                    if row and row[0]==Id:
                        continue # saute la ligne a supprimer
                    else:
                        list_salle_modified.append(row)
            with open(self.path_salle_csv,"w",newline="") as f:
                writer_s=csv.writer(f)
                writer_s.writerows(list_salle_modified) #enregistrement de toutes les salles dans le fichier csv
            print(f"La classe No: {Id} a ete supprimer avec succes")
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_salle_csv} n'existe pas !")

    """Methode pour afficher la liste de toutes les salles enregistrees"""
    def show_salles(self):
        list_salles=[]
        try:
            with open(self.path_salle_csv, "r") as f: #Ouverture du ficier de sauvegarde
                reader_s=csv.reader(f)
                header = next(reader_s,None)
                list_salles=[row for row in reader_s]
                if list_salles:
                    print(" | ".join(val.ljust(24) for val in header)) #Affiche de l'entete
                    print("-" * 120)
                    for row in list_salles:
                        print(" | ".join(val.ljust(24) for val in row)) #Affichage des ligne avec un espacement de 25 dans chaque colonne
                else:
                    print(f"Aucune Salle trouvee ")
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_salle_csv} n'existe pas !")

    def show_salle_id(self, id_salle:str,compt:int):
        header=["Id","Nom","Capacite_Maximale","Equipements","Horaire"] #Etntete de la liste

        salle=self.search_salle_by_id(id_salle) #Appel de la methode search_salle_by_id pour filtrer par id
        if salle:
            if compt==0: # pour afficcher l'entete uniquement dans la premiere iteration
                print(" | ".join(val.ljust(24) for val in header))
            salle_line=salle[0]
            print("-" * 120)
            print(" | ".join(val.ljust(24) for val in salle_line))



    """Methode pour rechercer une sallle avec son id , elle retourne la salle trouver"""
    def search_salle_by_id(self, Id:str):
        salle_found=[]
        try:
            with open(self.path_salle_csv, "r") as f: #Ouverture du ficier de sauvegarde
                reader_s=csv.reader(f)
                for row in reader_s:
                    if row and row[0].strip()==Id.strip():#Verification que l'Id correspond
                        salle_found.append(row)
                        break
            if not salle_found:
                print(f"Aucune Salle trouvee ")
            return salle_found #return de la salle ayant l'id preciser
        except FileNotFoundError:
            print(f"Le fichier correspondant au chemin {self.path_salle_csv} n'existe pas !")
            
    """Methode pour enregistrer une salle apres l'ajout dans le fichier csv"""
    def save_add_changes(self):
        with open(self.path_salle_csv, "a", newline="")as f:
            writer_s=csv.writer(f)
            header=["Id","Nom","Capacite_Maximale","Equipements","Horaire"]
            for el in self.salles:
                if(is_header_csv_exist(self.path_salle_csv,header)):
                    writer_s.writerow([el.id,el.nom,el.capacite_max,el.equipements,el.horaire])
                else:
                    writer_s.writerow(header)
                    writer_s.writerow([el.id,el.nom,el.capacite_max,el.equipements,el.horaire])
            self.salles=[]
        print("La Salle a ete enregistrer avec succes !")