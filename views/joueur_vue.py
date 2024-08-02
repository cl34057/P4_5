# Importation des modules et classes nécessaires
import datetime  # Importation du module datetime pour manipuler les dates
from controllers.joueur_controller import JoueurController  # Importation de la classe JoueurController
from models.joueur_model import Joueur, JoueurManager  # Importation des classes Joueur et JoueurManager

# Définition de la classe JoueurVue pour gérer l'interface utilisateur des joueurs
class JoueurVue:
    # Constructeur de la classe JoueurVue
    def __init__(self, gestion_joueur):
        self.gestion_joueur = gestion_joueur  # Référence à la fonction de gestion des joueurs
        self.joueur_controller = JoueurController()  # Création d'une instance de JoueurController

    # Méthode pour afficher le menu des joueurs
    def afficher_menu(self):
        print("===== Menu Joueur =====")
        print("1. Ajouter un joueur")
        print("2. Modifier un joueur")
        print("3. Supprimer un joueur")
        print("4. Afficher la liste des joueurs")
        print("5. Afficher les détails d'un joueur")
        print("6. Retour")

    # Méthode pour saisir les informations d'un joueur
    def saisir_joueur(self):
        while True:
            # Vérifie si le nombre maximal de joueurs est atteint
            if len(self.joueur_controller.joueur_manager.joueurs) >= JoueurManager.MAX_JOUEURS:
                print("Nombre maximal de joueurs atteint.")
                return None

            # Saisie des informations du joueur
            nom = self.saisir_champ_alpha("Nom du joueur : ")
            prenom = self.saisir_champ_alpha("Prénom du joueur : ")
            date_naissance = self.saisir_date_naissance()
            elo = self.saisir_elo()

            # Vérifie si le joueur existe déjà
            joueur_existant = self.joueur_controller.joueur_manager.trouver_joueur_par_details(
                nom, prenom, date_naissance
            )
            if joueur_existant:
                choix = input("CE JOUEUR EXISTE DÉJA. Voulez-vous ajouter un autre joueur ? (o/n) : ")
                if choix.lower() == 'o':
                    continue
                elif choix.lower() == 'n':
                    print("Retour au menu joueur.")
                    self.gestion_joueur()
                    return
                else:
                    print("Choix invalide. Veuillez répondre par 'o' ou 'n'.")
                    continue
            else:
                # Ajoute le nouveau joueur
                index = len(self.joueur_controller.joueur_manager.joueurs) + 1
                joueur = Joueur(index, nom, prenom, date_naissance, int(elo))
                self.joueur_controller.ajouter_joueur(joueur.nom, joueur.prenom, joueur.date_naissance, joueur.elo)

                choix = input("Voulez-vous ajouter un autre joueur ? (o/n) : ")
                if choix.lower() == 'o':
                    continue
                elif choix.lower() == 'n':
                    print("Retour au menu joueur.")
                    self.gestion_joueur()
                    return
                else:
                    print("Choix invalide. Veuillez répondre par 'o' ou 'n'.")
                    continue

    # Méthode pour modifier un joueur existant
    def modifier_joueur(self):
        index = self.saisir_index_joueur()
        if index is None:
            print("Modification annulée.")
            return
        joueur = self.joueur_controller.joueur_manager.joueurs[index - 1]
        print("===== Modifier le joueur =====")
        print(f"Nom : {joueur.nom}")
        print(f"Prénom : {joueur.prenom}")
        print(f"Date de naissance : {joueur.date_naissance}")
        print(f"Elo : {joueur.elo}")

        choix_modification = input("Voulez-vous modifier ce joueur ? (o/n) : ")
        if choix_modification.lower() == 'o':
            nom = input(f"Nouveau nom ({joueur.nom}) : ") or joueur.nom
            prenom = input(f"Nouveau prénom ({joueur.prenom}) : ") or joueur.prenom
            date_naissance = input(f"Nouvelle date de naissance ({joueur.date_naissance}) : ") or joueur.date_naissance
            elo = input(f"Nouvel elo ({joueur.elo}) : ") or joueur.elo
            self.joueur_controller.modifier_joueur(index, nom, prenom, date_naissance, elo)
            print("Joueur modifié avec succès.")
        else:
            print("Aucune modification effectuée.")

    # Méthode pour afficher les détails d'un joueur
    def afficher_joueur(self, joueur):
        print("===== Affichage des détails d'un joueur =====")
        print("Nom :", joueur.nom)
        print("Prénom :", joueur.prenom)
        print("Date de naissance :", joueur.date_naissance)
        print("Elo :", joueur.elo)

    # Méthode pour afficher la liste des joueurs
    def afficher_liste_joueurs(self):
        joueurs = self.joueur_controller.joueur_manager.joueurs
        print("===== Liste des Joueurs =====")
        for joueur in joueurs:
            print(f"Index: {joueurs.index(joueur) + 1}, Nom: {joueur.nom}, Prénom: {joueur.prenom}, "
                  f"Date_naissance: {joueur.date_naissance}, Elo: {joueur.elo}")

    # Méthode pour saisir l'index d'un joueur
    def saisir_index_joueur(self):
        joueurs = self.joueur_controller.joueur_manager.joueurs
        if not joueurs:
            print("Aucun joueur n'est disponible.")
            return None

        print("===== Liste des joueurs =====")
        for i, joueur in enumerate(joueurs, start=1):
            print(f"{i}. {joueur.nom} {joueur.prenom}")

        while True:
            try:
                index = int(input("Entrez l'index du joueur (ou 0 pour annuler) : "))
                if index == 0:
                    return None
                if 1 <= index <= len(joueurs):
                    return index
                else:
                    print("Index invalide. Veuillez entrer un index valide.")
            except ValueError:
                print("Veuillez entrer un nombre entier.")

    # Méthode pour saisir un champ alphabétique
    def saisir_champ_alpha(self, message):
        while True:
            valeur = input(message)
            if valeur.isalpha():
                return valeur
            print("Ce champ doit contenir uniquement des lettres.")

    # Méthode pour saisir la date de naissance d'un joueur
    def saisir_date_naissance(self):
        while True:
            date_naissance_str = input("Date de naissance du joueur (format YYYY-MM-DD) : ")
            try:
                return datetime.datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
            except ValueError:
                print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")

    # Méthode pour saisir le score Elo d'un joueur
    def saisir_elo(self):
        while True:
            elo = input("Elo du joueur (entre 1000 et 3500) : ")
            if elo.isdigit() and 1000 <= int(elo) <= 3500:
                return int(elo)
            print("Le score Elo doit être un entier compris entre 1000 et 3500.")