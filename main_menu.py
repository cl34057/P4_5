# Importation des modules nécessaires
from menu_tournoi import gestion_tournoi  # Importe la fonction gestion_tournoi du module menu_tournoi
from controllers.tournoi_controller import TournoiController  # Importe la classe TournoiController
from models.joueur_model import JoueurManager  # Importe la classe JoueurManager
from views.tournoi_vue import TournoiVue  # Importe la classe TournoiVue
import sys  # Importe le module sys pour les opérations système
from rapports import (
    liste_joueurs_alphabetique,
    details_tournoi,
    liste_joueurs_tournoi_alphabetique,
    liste_tours_et_matchs
)  # Importe les fonctions de rapport


# Définition de la fonction du menu principal
def main_menu() -> None:
    
    tournoi_controller = TournoiController()  # Crée une instance de TournoiController
    joueur_manager = JoueurManager()  # Crée une instance de JoueurManager
    tournoi_vue = TournoiVue(tournoi_controller, joueur_manager)  # Crée une instance de TournoiVue

    while True:  # Boucle principale du menu
        print("===== Gestion des Joueurs et Tournois =====")
        print("1. Gestion des Joueurs")
        print("2. Gestion des Tournois")
        print("3. Générer des Rapports")
        print("4. Quitter")
        choix = input("Entrez votre choix : ")  # Demande le choix de l'utilisateur

        if choix == "1":
            from menu_joueur import gestion_joueur  # Importe la fonction gestion_joueur
            gestion_joueur()  # Appelle la fonction gestion_joueur
        elif choix == "2":
            gestion_tournoi(tournoi_vue)  # Appelle la fonction gestion_tournoi
        elif choix == "3":
            generer_rapports(tournoi_controller, joueur_manager, tournoi_vue)  # Appelle la fonction generer_rapports
        elif choix == "4":
            print("Merci d'avoir utilisé l'application. À bientôt !")
            sys.exit()  # Quitte l'application
        else:
            print("Choix invalide. Veuillez réessayer.")

# Définition de la fonction pour générer des rapports
def generer_rapports(
    tournoi_controller: TournoiController,
    joueur_manager: JoueurManager,
    tournoi_vue: TournoiVue
) -> None:
    while True:  # Boucle du menu des rapports
        print("===== Menu Rapports =====")
        print("1. Liste des joueurs par ordre alphabétique")
        print("2. Nom et Date d'un tournoi")
        print("3. Liste des joueurs d'un tournoi par ordre alphabétique")
        print("4. Liste des rondes et matchs d'un tournoi")
        print("5. Retour")
        choix = input("Entrez votre choix : ")  # Demande le choix de l'utilisateur

        if choix == "1":
            joueurs = joueur_manager.charger_joueurs()  # Charge la liste des joueurs
            if joueurs:
                print(liste_joueurs_alphabetique(joueurs))  # Affiche la liste des joueurs par ordre alphabétique
            else:
                print("Aucun joueur n'est enregistré.")
        elif choix == "2":
            index_tournoi = tournoi_vue.saisir_index_tournoi()  # Demande l'index du tournoi
            if index_tournoi is not None:
                # Trouve le tournoi
                tournoi = tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  
                if tournoi:
                    print(details_tournoi(tournoi))  # Affiche les détails du tournoi
                else:
                    print("Tournoi non trouvé.")
        elif choix == "3":
            index_tournoi = tournoi_vue.saisir_index_tournoi()  # Demande l'index du tournoi
            if index_tournoi is not None:
                 # Trouve le tournoi
                tournoi = tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi) 
                if tournoi:
                    print(liste_joueurs_tournoi_alphabetique(tournoi))  # Affiche la liste des joueurs du tournoi
                else:
                    print("Tournoi non trouvé.")
        elif choix == "4":
            index_tournoi = tournoi_vue.saisir_index_tournoi()  # Demande l'index du tournoi
            if index_tournoi is not None:
                # Trouve le tournoi
                tournoi = tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi) 
                if tournoi:
                    print(f"Nombre de rondes dans le tournoi : {len(tournoi.rondes)}")
                    for ronde in tournoi.rondes:
                        print(f"Ronde {ronde.numero} - Nombre de matchs : {len(ronde.matchs)}")
                    resultat = liste_tours_et_matchs(tournoi)  # Obtient la liste des tours et matchs
                    print(resultat)  # Affiche la liste des tours et matchs
                else:
                    print("Tournoi non trouvé.")
            else:
                print("Index de tournoi invalide.")
        elif choix == "5":
            break  # Retourne au menu principal
        else:
            print("Choix invalide. Veuillez réessayer.")

# Point d'entrée du programme
if __name__ == "__main__":
    main_menu()  # Appelle la fonction du menu principal
