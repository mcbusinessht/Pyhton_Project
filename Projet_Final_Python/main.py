from models.salles import Salle ,GestionnaireSalle
from models.evenements import Evenement ,PlanificationEvenements
from models.reservations import ReservationSalle, Reservation
from datetime import datetime
from utils.fct_utiles import add_horaire , generate_id , verify_hours, verify_id_exist, get_salles_id

def run():
    gestion_Salle=GestionnaireSalle()
    gestion_res=ReservationSalle()
    gestion_events=PlanificationEvenements()
    gestion_events.update_events()

    #Menu Principale de l'application
    print("\nBienvenue dans notre Systeme de reservation (salles,evenemens, ...)")
    while True:
        print("\n","-"*50,"Menu Principal","-"*50)
        c=input("1. Gestions des salles \n2. Gestion des evenements \n3. Gestion des reservations \n4. Rapports et Statistiques\n5. Quitter le systeme\nRep_: ")
        if c in ('1','2','3','4','5'):


            match c: # les differentes cases principale de l'application , 5 en tout
                case '1':
                    while True:
                        print("\n","-"*54,"Menu 2","-"*54)
                        c_two=input("1. Liste des salles\n2. Ajouter une nouvelle salle \n3. Modifier une salle \n4. Supprimer une salle \n5. Revenir au mrnu principal \nRep_: ")
                        match c_two:    
                            case '1':
                                gestion_Salle.show_salles()
                                        
                            case '2':
                                while True:
                                    name_salle=input("\nSaisissez le nom de la salle \nRep:_ ")
                                    equipemement=[]
                                    while True: 
                                        try:
                                            cap_max=int(input("\nSaisissez la capaciter maximale de la salle(nbre de personne) ex: 50\nRep_: "))
                                            break
                                        except ValueError:
                                            print("Erreur, veuillez entrer un chiffre valide")
                                    while True:
                                        c_three=input("\n1. Ajouter un equipement \n2. Terminer l'enregistrement de la salle\nRep_: ")
                                        if c_three=='1':
                                            value=input("\nEntrez le nom de l'equipement \nRep_: ")
                                            equipemement.append(value)
                                        elif c_three=='2':
                                            break 
                                    print("\nHoraire : ")                
                                    horaire=add_horaire()
                                    id_salle= generate_id(GestionnaireSalle.path_salle_csv)
                                    new_salle=Salle(id_salle,name_salle,cap_max,equipemement,horaire)
                                    gestion_Salle.add_salle(new_salle)
                                    gestion_Salle.save_add_changes()
                                    print("\nInformation de la Salle enregistrer")
                                    print(f"Id                 : {id_salle}")
                                    print(f"Nom                : {name_salle}")
                                    print(f"Capaciter maximale : {cap_max} personne(s)")
                                    print(f"Equipements        : {equipemement}")
                                    print(f"Horaire            : {horaire}")

                                    break
                            case '3':
                                while True:
                                    c_two=input("\n1. Voir la liste des Salles \n2. Modifer une salle avec son ID\n3. Revenir au menu 2 \nRep_: ")
                                    if c_two=='1':
                                        gestion_Salle.show_salles()
                                    elif c_two=='2':
                                        while True:
                                            try:
                                                Id=int(input("\nEntrez l'Id de la classe que vous souhaitez modifier\nRep_: "))
                                                salle_id=gestion_Salle.search_salle_by_id(f"{Id}")
                                                first_salle=salle_id[0]
                                                print(f"\n--------------------------Informations de la salle ayant l'Id--------------------------{Id}")
                                                print(f"Id                 : {first_salle[0]}")
                                                print(f"Nom                : {first_salle[1]}")
                                                print(f"Capaciter maximale : {first_salle[2]} personne(s)")
                                                print(f"Equipements        : {first_salle[3]}")
                                                print(f"Horaire            : {first_salle[4]}")                                                
                                                name_salle=input("\nSaisissez le nouveau nom de la salle \nRep:_ ")
                                                equipemement=[]
                                                while True: 
                                                    try:
                                                        cap_max=int(input("\nSaisissez la capaciter maximale de la salle(nbre de personne) ex: 50\nRep_: "))
                                                        break
                                                    except ValueError:
                                                        print("Erreur, veuillez entrer un chiffre valide")
                                                while True:
                                                    c_three=input("\n1. Ajouter un equipement \n2. Terminer l'enregistrement de la salle\nRep_: ")
                                                    if c_three=='1':
                                                        value=input("\nEntrez le nom de l'equipement \nRep_: ")
                                                        equipemement.append(value)
                                                    elif c_three=='2':
                                                        break 
                                                print("\nHoraire d'ouverture")                
                                                horaire=add_horaire()
                                                new_salle=Salle(f"{Id}",name_salle,cap_max,equipemement,horaire)
                                                gestion_Salle.edit_salle(f"{Id}",new_salle)
                                                break
                                            except ValueError:
                                                print("Erreur, Id saisie invalid") 
                                    elif c_two=='3':
                                        break
                                    else:
                                        print("Erreur, Saisie Incoorecte")                   
                            case '4':
                                while True:
                                    c_two=input("\n1. Voir la liste des Salles \n2. Supprimer une salle avec son ID \n3. Revenir au menu 2\nRep_: ")
                                    if c_two=='1':
                                        salles=gestion_Salle.show_salles()
                                        print(salles)
                                    elif c_two=='2':
                                        while True:
                                            try:
                                                Id=int(input("Entrez l'Id de la Salle que vous souhaitez Supprimer\nRep_: "))
                                                salle_id=gestion_Salle.search_salle_by_id(f"{Id}")
                                                first_salle=salle_id[0]
                                                print(f"\n--------------------------Informations de la salle ayant l'Id {Id}--------------------------")
                                                print(f"Id                 : {first_salle[0]}")
                                                print(f"Nom                : {first_salle[1]}")
                                                print(f"Capaciter maximale : {first_salle[2]} personne(s)")
                                                print(f"Equipements        : {first_salle[3]}")
                                                print(f"Horaire            : {first_salle[4]}")                                                    
                                                while True:
                                                    c_three=input("1. Supprimer cette salle sans retour possible\n2. Annuler la suppresion\nRep_: ")
                                                    if c_three=='1':
                                                        gestion_Salle.delete_salle(f"{Id}")
                                                        break
                                                    elif c_three=='2':
                                                        break
                                            except ValueError:
                                                print("Erreur, Id saisie invalid")
                                            break  
                                    elif c_two=='3':  
                                        break
                                    else:
                                        print("Erreur, Saisie Incoorecte")  
                            case '5':
                                break    
                            case _:
                                print("Erreur, Saisie Invalid")
                case '2':
                    gestion_events.update_events()
                    while True :
                        print("\n","-"*54,"Menu 2","-"*54)
                        c_two=input("1. Ajouter un nouvel evenement \n2. Liste des evenements\n3. Mettre a jour un evenement \n4. Annuler un evenement \n5. Revenir au menu principal \nRep_: ")
                        match c_two:
                            case '1':
                                name_event=input("\nEntrez le nom de l'evenement\nRep_: ")
                                horaire=""
                                while True:
                                    date_str=input("\nEntrez la date de l'evenement dans le format (YYYY-MM-DD)\nRep_: ")
                                    try:
                                        date_event = datetime.strptime(date_str,"%Y-%m-%d")
                                        today=datetime.now()
                                        if date_event < today :
                                            print("Erreur, la date doit etre une date future")
                                        else:
                                            horaire = date_str
                                            while True:
                                                hour=input("\nEntrez l'heure de debut et l'heure de fin dans le format HH:MM-HH:MM ex: 07:30-16:00\nRep:_ ")
                                                flag=verify_hours(hour)
                                                if flag:
                                                    horaire=horaire +"|"+hour
                                                    break
                                            break
                                    except ValueError:
                                        print("Erreur, format de date  saisie incorrecte\n")                                
                                while True:
                                    try:
                                        nbre_participant=int(input("\nEntrez le nombre de participant prevu pour cet evenement\nRep_: "))
                                        break
                                    except ValueError:
                                        print("Error, Veuillez entrer un nombre correcte")
                                events_path=PlanificationEvenements.path_event_csv
                                id_event=generate_id(events_path)
                                event=Evenement(id_event,name_event,horaire,nbre_participant)
                                gestion_events.add_event(event)
                                gestion_events.save_add_changes()
                                print("\nInformation de l'evenement enregistrer")
                                print(f"Id                    : {id_event}")
                                print(f"Nom                   : {name_event}")
                                print(f"Horaire               : {horaire} ")
                                print(f"Nombre de participant : {nbre_participant} personne(s)")

                            case '2':
                                while True:
                                    c_three=input("\n1. Lister tout les evenements\n2. Lister les evenements d'une salle \n3. Revenir au menu 2\nRep_: ")
                                    if c_three=='1':
                                        events=gestion_events.show_events()
                                    elif c_three=='2':
                                        while True:
                                            try:
                                                id_salle=int(input("\nEntrez l'id de la salle \nRep_: "))
                                                events=gestion_events.show_events_per_salle(f"{id_salle}")
                                                break
                                            except ValueError:
                                                print("Erreur, Saisie incorrecte")
                                        break
                                    elif c_three=='3':
                                        break
                                    else:
                                        print("Erreur, saisie incorrecte")
                            case '3':
                                while True:
                                    try:
                                        Id=input("Entrez l'id de l'evenement a mettre a jour ou 0 pour annuler la mise a jour\nRep_: ")
                                        if Id=='0':break
                                        event_id=gestion_events.search_event_by_id(f"{Id}")
                                        if event_id : 
                                            first_event=event_id[0]
                                            if first_event and first_event[5]=="Annuler":
                                                print("\nImpossible de mettre a jour cet evenement car elle a ete annuler\nCreer un autre evement !")
                                            elif event_id :
                                                while True:
                                                    c_s=input("\n1. Mettre a jour le Statut de l'evement \n2. Mettre a jour tout l'evenement\nRep_: ")
                                                    if c_s in ('1','2'):break
                                                    else: print("Erreur, saisie Incorecte------")
                                                if c_s == '1':
                                                    print(f"\n--------------------------Informations de l'evenemnt ayant l'Id {Id}--------------------------")
                                                    print(f"Id                    : {first_event[0]}")
                                                    print(f"Nom                   : {first_event[1]}")
                                                    print(f"Horaire               : {first_event[2]} ")
                                                    print(f"Nombre de participant : {first_event[3]} personne(s)")
                                                    print("\nStatus possible : ")
                                                    statut_choice=("En attente","En cours","Terminer","Annuler")
                                                    for el in statut_choice:
                                                        print(statut_choice.index(el)+1," -",el)
                                                    while True:
                                                        new_statut=input("\nSelectionner le nouveau statut de l'evement : \nRep_: ")
                                                        if new_statut in ('1','2','3','4'):break
                                                        else:print("Erreur, saisie incorrecte")
                                                    first_event[5]=statut_choice[int(new_statut)-1]
                                                    event=Evenement(first_event[0],first_event[1],first_event[2],first_event[4])
                                                    event.change_salle_reserver(first_event[3])
                                                    event.change_status(first_event[5])
                                                    gestion_events.edit_evenement(Id,event)
                                                elif c_s=='2':
                                                    print(f"\n--------------------------Informations de l'evenement ayant l'Id {Id}--------------------------")
                                                    print(f"Id                    : {first_event[0]}")
                                                    print(f"Nom                   : {first_event[1]}")
                                                    print(f"Horaire               : {first_event[2]} ")
                                                    print(f"Nombre de participant : {first_event[3]} personne(s)")                                            
                                                    name_event=input("\nEntrez le nouveau nom de l'evenement ou le meme nom\nRep_: ")
                                                    horaire=""
                                                    while True:
                                                        date_str=input("\nEntrez la date de l'evenement dans le format (YYYY-MM-DD)\nRep_: ")
                                                        try:
                                                            date_event = datetime.strptime(date_str,"%Y-%m-%d")
                                                            today=datetime.now()
                                                            if date_event < today :
                                                                print("Erreur, la date doit etre une date future")
                                                            else:
                                                                horaire = date_str
                                                                while True:
                                                                    hour=input("\nEntrez l'heure de debut et l'heure de fin dans le format HH:MM-HH:MM ex: 07:30-16:00\nRep:_ ")
                                                                    flag=verify_hours(hour)
                                                                    if flag:
                                                                        horaire=horaire +"|"+hour
                                                                        break
                                                                break
                                                        except ValueError:
                                                            print("Erreur, format de date saisie incorrecte\n")
                                                    while True:
                                                        try:
                                                            nbre_participant=int(input("\nEntrez le nombre de participant prevu pour cet evenement\nRep_: "))
                                                            break
                                                        except ValueError:
                                                            print("Error, Veuillez entrer un nombre correcte")
                                                    event=Evenement(Id,name_event,horaire,nbre_participant)
                                                    gestion_events.edit_evenement(Id,event)
                                                    break
                                        else:
                                            print("Id non trouve")
                                    except ValueError:
                                        print("Erreur, Veuillez entrer un Id valide")
                                
                            case '4':
                                while True :
                                    try:
                                        del_event = int(input("Entrez l'Id de l'evenement a Annuler ou 0 pour Annuler l'annulation\nRep_: "))
                                        if del_event==0:
                                            break

                                        event_id=gestion_events.search_event_by_id(f"{del_event}")
                                        if event_id : 
                                            first_event=event_id[0]
                                            print(f"\n--------------------------Informations de la salle ayant l'Id {del_event}--------------------------")
                                            print(f"Id: {first_event[0]} \nNom : {first_event[1]} \nDate, heure debut et fin : {first_event[2]}\nId salle reserver : {first_event[3]}\nNbre de personne : {first_event[4]}  \nStatut : {first_event[5]} ")
                                            while True:
                                                new_statut=input("\n1. Confirmer l'annulation \n2. Quitter l'annulation \nRep_: ")
                                                if new_statut =='1':
                                                    event=Evenement(first_event[0],first_event[1],first_event[2],first_event[4])
                                                    event.change_salle_reserver(first_event[3])
                                                    event.change_status("Annuler")
                                                    gestion_events.edit_evenement(f"{del_event}",event)
                                                    break
                                                elif new_statut=='2':
                                                    break
                                                else:print("Erreur, saisie incorrecte")
                                        else:print("Erreur, Id invalid")
                                    except ValueError:
                                        print("Veuilez entrer un Id correct")


                            case '5':
                                break
                            case _:
                                print("\nErreur, saisie incorrete\n")
                case '3':
                    while True:
                        print("\n","-"*54,"Menu 2","-"*54)
                        print("1. Liste des reservations \n2. Reserver une salle pour un Evenement \n3. Consulter la disponibilitee des salles en temps reel")
                        c_two=input("4. Retour au menu principale \nRep_: ")
                        match c_two:
                            case '1':
                                while True:
                                    c_three=input("\n1. Liste de toute les reservations \n2. Rechercher une reservation avec son Id\n3. Revenir au menu 2\nRep_: ")
                                    if c_three=='1':
                                        gestion_res.show_reservation()
                                        break
                                    elif c_three=='2':
                                        while True:
                                            try:
                                                id_r=int(input("\nEntrez l'id de la reservation\nRep_: \n"))
                                                gestion_res.show_reservation_by_id(f"{id_r}",0)
                                                break
                                            except ValueError:
                                                print("Erreur, format de l'Id incalid !")
                                        break
                                    elif c_three=='3':
                                        break
                                    else:
                                        print("Erreur, saisie invalide !")
                            case '2':
                                while True:
                                    id_event=input("\nEntrez l'id de l'evenement \nRep_: ")
                                    flag_e=verify_id_exist(PlanificationEvenements.path_event_csv, id_event)
                                    if flag_e:
                                        while True:
                                            id_salle=input("\nEntrez l'id de la salle a reserver\nRep_: ")
                                            flag_s=verify_id_exist(gestion_Salle.path_salle_csv,id_salle)
                                            if flag_s:
                                                id_res=generate_id(ReservationSalle.path_reservation_csv)
                                                res=Reservation(id_res,id_salle,id_event)
                                                is_add=gestion_res.add_reservation(res)
                                                if is_add:                                           
                                                    event_s=gestion_events.search_event_by_id(id_event)
                                                    event_s_1=event_s[0]
                                                    event=Evenement(event_s_1[0],event_s_1[1],event_s_1[2],event_s_1[4])
                                                    event.change_salle_reserver(id_salle)
                                                    gestion_events.edit_evenement(event_s_1[0],event)

                                                    
                                                break
                                            else:
                                                print("Id de la salle introuvable")
                                        break
                                    else:
                                        print("Id de l'evenement introuvable")
                            case '3':
                                while True:
                                    print("\n1. Voir la liste de toute les salles et leurs disponibiliter\n2. Voir la disponibiliter pour une salle specifique")
                                    c_three=input("3. Retour a menu 2 \nRep_: ")
                                    if c_three=='1':
                                        print ("\nListe des salles et de leurs disponibiliter en temps reel ")
                                        list_salle_id=get_salles_id(gestion_Salle.path_salle_csv)
                                        for el in list_salle_id:
                                            gestion_events.show_disponibility_salle(el)
                                        break
                                    elif c_three=='2':
                                        try:
                                            id_s=int(input("\nEntrez l'Id le la salle \nRep_: "))
                                            if gestion_Salle.search_salle_by_id(f"{id_s}"):
                                                gestion_events.show_disponibility_salle(f"{id_s}")
                                        except ValueError:
                                            print("Erreur, saisie invalide !")
                                        break
                                    elif c_three=='3':
                                        break
                                    else:
                                        print("Erreur, saisie invalide !")
                            case '4':
                                break
                            
                            case _:
                                print("Erreur, Saisie Invalid !")
                case '4':
                    gestion_events.update_events()
                    while True:
                        print("\n","-"*54,"Menu 2","-"*54)
                        print("\nRapports et Statistiques")
                        print("1. Liste des salles reservees pour(la journnee, la semaine, le mois)")
                        c_three=input("2. Historique des evenements \n3. Revenir au Principale\nRep_: ")
                        if c_three=='1':
                            while True:
                                print("\nListe des salles reservees :")
                                period=input("1. Pour la journee (Aujourd'hui) \n2. Pour la semaine \n3. Pour le mois \n4. Revenir au menu 2\nRep_: ")
                                if period=='1':
                                    reports= gestion_res.generate_report("day")
                                    if reports:
                                        print("\nListe des reservations de salle realiser pour aujourd'hui")
                                        gestion_res.show_report(reports)
                                    else:
                                        print("Aucune reservation n'a ete realiser pour aujourd'hui")
                                    
                                elif period=='2':
                                    reports= gestion_res.generate_report("week")
                                    if reports:
                                        print("\nListe des reservations de salle realiser pour cette semaine :")
                                        gestion_res.show_report(reports)
                                    else:
                                        print("Aucune reservation n'a ete realiser pour cette semaine")

                                elif period=='3':
                                    reports= gestion_res.generate_report("month")
                                    if reports:
                                        print("\nListe des reservations de salle realiser pour ce mois")
                                        gestion_res.show_report(reports)
                                    else:
                                        print("Aucune reservation n'a ete realiser pour ce mois")  

                                elif period=='4':
                                    break        
                                else:
                                    print("Erreur, saisie invalide !")
                        elif c_three=='2':
                            print("\nHistorique des evenemnts Terminer\n")
                            list_event=gestion_events.history_event()
                            for first_event in list_event:
                                print(f"Id                    : {first_event[0]}")
                                print(f"Nom                   : {first_event[1]}")
                                print(f"Horaire               : {first_event[2]} ")
                                print(f"Id salle reservee     : {first_event[3]} ")
                                print(f"Nombre de participant : {first_event[4]}  personne(s)")
                                print(f"Statut                : {first_event[5]} ")

                                print("\n")

                        elif c_three=='3':
                            break
                        else:
                            print("Erreur, saisie invalide")
                case '5':
                    break
                case _:
                    print("Erreur, Saisie Invalid !")
            if c_two==5: 
                continue
            
        
if __name__=="__main__":    
    run()





