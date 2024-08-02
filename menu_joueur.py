# Importation de la classe JoueurVue depuis le module views.joueur_vue
from views.joueur_vue import JoueurVue


# Définition de la fonction gestion_joueur
def gestion_joueur():
    # Importation de la fonction main_menu depuis le module main_menu
    from main_menu import main_menu
    # Création d'une instance de JoueurVue avec la fonction gestion_joueur comme paramètre
    joueur_vue = JoueurVue(gestion_joueur)

    # Boucle principale pour la gestion des joueurs
    while True:
        # Affichage du menu des joueurs
        joueur_vue.afficher_menu()
        # Demande à l'utilisateur de faire un choix
        choix = input("Entrez votre choix : ")

        # Traitement du choix de l'utilisateur
        if choix == "1":
            # Si l'ajout de joueur réussit, continue la boucle
            if joueur_vue.saisir_joueur() is True:
                continue
            # Si le nombre maximal de joueurs est atteint, affiche un message
            elif len(joueur_vue.joueur_controller.joueur_manager.joueurs) >= JoueurManager.MAX_JOUEURS:
                print("Le nombre maximal de joueurs est déjà atteint.")
            # Sinon, ajoute le nouveau joueur
            else:
                joueur = joueur_vue.saisir_joueur()
                joueur_vue.joueur_controller.ajouter_joueur(
                    joueur.nom, joueur.prenom, joueur.date_naissance, joueur.elo
                )
        elif choix == "2":
            # Appelle la méthode pour modifier un joueur
            joueur_vue.modifier_joueur()
        elif choix == "3":
            # Appelle la méthode pour supprimer un joueur
            joueur_vue.supprimer_joueur()
        elif choix == "4":
            # Appelle la méthode pour afficher la liste des joueurs
            joueur_vue.afficher_liste_joueurs()
        elif choix == "5":
            # Appelle la méthode pour afficher les détails d'un joueur
            joueur_vue.afficher_details_joueur()
        elif choix == "6":
            # Retourne au menu principal
            print("Retour au menu principal")
            main_menu()
            return
        else:
            # Affiche un message d'erreur pour un choix invalide
            print("Choix invalide. Veuillez réessayer.")
    return


# Vérifie si le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    # Appelle la fonction gestion_joueur
    gestion_joueur()