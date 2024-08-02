# Importation de la classe TournoiVue depuis le module views.tournoi_vue
from views.tournoi_vue import TournoiVue


# Définition de la fonction gestion_tournoi qui prend un objet TournoiVue en paramètre
def gestion_tournoi(tournoi_vue: TournoiVue) -> None:
    while True:  # Boucle infinie pour afficher le menu et gérer les choix de l'utilisateur
        tournoi_vue.afficher_menu()  # Affiche le menu des options du tournoi
        choix = input("Entrez votre choix : ")  # Demande à l'utilisateur de saisir son choix

        # 1-Création Nouveau Tournoi
        if choix == "1":
            # Saisit les informations du nouveau tournoi
            nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi = tournoi_vue.saisir_tournoi()
            # Ajoute le nouveau tournoi via le contrôleur et affiche un message selon le résultat
            if tournoi_vue.tournoi_controller.tournoi_manager.ajouter_tournoi(
                nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi
            ):
                print("Tournoi ajouté avec succès.")
            else:
                print("Erreur lors de l'ajout du tournoi.")

        # 2- Modifier tournoi
        elif choix == "2":
            while True:  # Boucle pour gérer les sous-options de modification de tournoi
                print("===== Menu Modifier tournoi =====")
                print("a. Modification d'un tournoi")
                print("b. Ajouter un joueur au tournoi")
                print("c. Supprimer un joueur du tournoi")
                print("d. Retour au menu principal")
                sous_choix = input("Entrez votre choix : ")  # Demande à l'utilisateur de saisir son choix

                if sous_choix == "a":
                    tournoi_vue.modifier_tournoi()  # Appelle la méthode pour modifier un tournoi
                    input("\nAppuyez sur Entrée pour continuer...")
                elif sous_choix == "b":
                    index_tournoi = tournoi_vue.saisir_index_tournoi()  # Saisit l'index du tournoi
                    tournoi_vue.saisir_joueurs_participants(index_tournoi)  # Ajoute un joueur au tournoi
                    print("Joueur ajouté au tournoi avec succès.")
                    input("\nAppuyez sur Entrée pour continuer...")
                elif sous_choix == "c":
                    index_tournoi = tournoi_vue.saisir_index_tournoi()  # Saisit l'index du tournoi
                    tournoi_vue.supprimer_joueur_tournoi(index_tournoi)  # Supprime un joueur du tournoi
                    print("Joueur supprimé du tournoi avec succès.")
                    input("\nAppuyez sur Entrée pour continuer...")
                elif sous_choix == "d":
                    break  # Retourne au menu principal
                else:
                    print("Choix invalide. Veuillez réessayer.")

        # 3- Supprimer tournoi
        elif choix == "3":
            index_tournoi = tournoi_vue.saisir_index_tournoi()  # Saisit l'index du tournoi
            # Supprime le tournoi via le contrôleur et affiche un message selon le résultat
            if tournoi_vue.tournoi_controller.tournoi_manager.supprimer_tournoi(index_tournoi):
                print("Tournoi supprimé avec succès.")
            else:
                print("Erreur lors de la suppression du tournoi.")

        # 4- Afficher liste des tournois
        elif choix == "4":
            tournoi_vue.afficher_liste_tournois()  # Affiche la liste des tournois

        # 5- Afficher details d'un tournoi
        elif choix == "5":
            index_tournoi = tournoi_vue.saisir_index_tournoi()  # Saisit l'index du tournoi
            tournoi = tournoi_vue.afficher_details_tournoi(index_tournoi)  # Affiche les détails du tournoi
            if tournoi:
                while True:  # Boucle pour gérer les sous-options des détails du tournoi
                    print("1. détails d'un tournoi")
                    print("2. Créer une ronde")
                    print("3. Saisir les résultats d'une ronde")
                    print("4. Jouer une ronde")
                    print("5. Afficher le classement")
                    print("6. Retour")
                    option = input("Sélectionnez une option : ")  # Demande à l'utilisateur de saisir son choix

                    if option == "1":
                        tournoi_vue.afficher_details_tournoi(index_tournoi)  # Affiche les détails du tournoi
                    elif option == "2":
                        tournoi.creer_ronde()  # Crée une nouvelle ronde
                        print("Ronde créée avec succès.")
                    elif option == "3":
                        numero_ronde = int(input("Entrez le numéro de la ronde : "))  # Saisit le numéro de la ronde
                        tournoi.saisir_resultats_ronde(numero_ronde)  # Saisit les résultats de la ronde
                    elif option == "4":
                        tournoi.jouer_ronde()  # Joue une ronde
                    elif option == "5":
                        print("Classement :")
                        # Affiche le classement des joueurs
                        for ligne in tournoi.classement():
                            print(f"{ligne[0].nom} {ligne[0].prenom} : {ligne[1]} points")
                    elif option == "6":
                        break  # Retourne au menu principal
                    else:
                        print("Option invalide.")

        # 6- Quitter
        elif choix == "6":
            break  # Quitte la boucle et termine la fonction

        else:
            print("Choix invalide. Veuillez réessayer.")  # Message d'erreur pour choix invalide


# Bloc principal du programme
if __name__ == "__main__":
    # Importation des modules nécessaires pour le bloc principal
    from controllers.tournoi_controller import TournoiController
    from models.joueur_model import JoueurManager

    tournoi_controller = TournoiController()  # Création d'une instance de TournoiController
    joueur_manager = JoueurManager()  # Création d'une instance de JoueurManager
    tournoi_vue = TournoiVue(tournoi_controller, joueur_manager)  # Création d'une instance de TournoiVue

    gestion_tournoi(tournoi_vue)  # Appel de la fonction gestion_tournoi avec l'instance de TournoiVue