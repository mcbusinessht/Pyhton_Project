import csv 
import random
import re
def is_header_csv_exist(path_csv:str,normal_format:list)->bool:
    with open(path_csv, "r+") as f:
        reader_f=csv.reader(f)
        first_line=next(reader_f,None)
        return first_line==normal_format
    
def generate_id(path_csv:str)->str:
    try:
        with open(path_csv,"r")as f:
            reader_f=csv.reader(f)
            while True:
                id= random.randrange(100000,999999)
                if(any(row[0] ==id for row in reader_f)):
                    continue
                else:
                    return f"{id}"
    except FileNotFoundError:
        print("Fichier introuvale")
def get_salles_id(path_salle_csv:str)->list:
    list_salle_id=[]
    try:
        with open(path_salle_csv, 'r') as f:
            reader_s=csv.reader(f)
            header= next(reader_s,None)
            for row in reader_s:
                list_salle_id.append(row[0])
            return list_salle_id
    except FileNotFoundError:
        print("Fichier introuvale")




def verify_id_exist(path_csv:str,Id:str):
    try:
        with open(path_csv, "r") as f:
            reader_f=csv.reader(f)
            for row in reader_f:
                if row and row[0]==Id:
                    return True
            return False


    except FileNotFoundError:
        print("Fichier introuvale")

def verify_hours(hours:str)->bool:
    if re.match(r"^([01]?[0-9]|2[0-3]):([0-5][0-9])-([01]?[0-9]|2[0-3]):([0-5][0-9])$", hours):
        heure_debut, minute_debut, heure_fin, minute_fin = map(int, re.findall(r"\d+", hours))

        if 0 <= heure_debut < 24 and 0 <= minute_debut < 60 and 0 <= heure_fin < 24 and 0 <= minute_fin < 60:
            if heure_debut < heure_fin or (heure_debut == heure_fin and minute_debut < minute_fin):
                return True
            else:
                print(f"Erreur : l'heure de début doit être avant l'heure de fin")
                return False
        else:
            print("Les valeurs d'heure ou de minutes sont incorrectes")
            return False
    else:
        print(f"Le format de l'horaire est incorrect")
        return False
        
def add_horaire()->str:
    while True:
        hours=input("Entrez l'heure d'ouverture et de fermeture dans le format HH:MM-HH:MM ex: 07:30-16:00\nRep:_ ")
        is_hours_good=verify_hours(hours)
        if is_hours_good:
            return hours
        
                            
                            