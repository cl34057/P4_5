# Importation des modules nécessaires
import datetime  # Pour manipuler les dates
import re  # Pour les expressions régulières
import json  # Pour manipuler les fichiers JSON
from typing import Optional  # Pour les annotations de type optionnelles

# Importation des classes nécessaires depuis les modules correspondants
from controllers.tournoi_controller import TournoiController  # Contrôleur pour les tournois
from models.joueur_model import Joueur, JoueurManager  # Modèles pour les joueurs et gestion des joueurs

# Définition de la classe TournoiVue pour gérer l'interface utilisateur des tournois
class TournoiVue:
    # Constructeur de la classe TournoiVue
    def __init__(self, tournoi_controller: TournoiController, joueur_manager: JoueurManager):
        self.tournoi_controller = tournoi_controller  # Initialisation du contrôleur de tournoi
        self.joueur_manager = joueur_manager  # Initialisation du gestionnaire de joueurs

    # Méthode pour afficher le menu principal des tournois
    def afficher_menu(self) -> None:
        print("===== Menu Tournoi =====")
        print("1. Créer un nouveau tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Afficher les détails d'un tournoi")
        print("6. Retour")

    # Méthode pour saisir les informations d'un nouveau tournoi
    def saisir_tournoi(self) -> tuple:
        while True:
            nom = input("Nom du tournoi : ")  # Saisie du nom du tournoi
            if not re.match("^[a-zA-Z0-9 ]+$", nom):  # Vérification du format du nom
                print("Le nom du tournoi doit contenir uniquement des caractères alphanumériques et peut contenir des espaces.")
                continue
            
            date_debut = input("Date de début (format YYYY-MM-DD) : ")  # Saisie de la date de début
            date_fin = input("Date de fin (format YYYY-MM-DD) : ")  # Saisie de la date de fin
            
            try:
                # Conversion des dates saisies en objets date
                date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
                date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
                
                if date_fin < date_debut:  # Vérification que la date de fin est postérieure à la date de début
                    print("La date de fin doit être ultérieure à la date de début.")
                    continue
                
                nb_max_joueurs = int(input("Nombre maximal de joueurs : "))  # Saisie du nombre maximal de joueurs
                nb_rondes = int(input("Nombre de rondes : "))  # Saisie du nombre de rondes
                type_tournoi = input("Type de tournoi : ")  # Saisie du type de tournoi
                
                # Retourne les informations saisies sous forme de tuple
                return nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi
            
            except ValueError:
                print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")

    # Méthode pour modifier un tournoi existant
    def modifier_tournoi(self) -> None:
        index = self.saisir_index_tournoi()  # Saisie de l'index du tournoi à modifier
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index)  # Recherche du tournoi par index
        
        if not tournoi:  # Vérification si le tournoi existe
            print("Tournoi non trouvé.")
            return
        
        print("===== Modifier le tournoi =====")
        print(f"Nom du tournoi : {tournoi.nom}")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre maximal de joueurs : {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes : {tournoi.nb_rondes}")
        print(f"Type de tournoi : {tournoi.type_tournoi}")
        
        choix_modification = input("Voulez-vous modifier ce tournoi ? (o/n) : ")  # Demande de confirmation pour la modification
        
        if choix_modification.lower() == 'o':
            # Saisie des nouvelles informations ou conservation des anciennes si aucune saisie
            nom = input(f"Nouveau nom du tournoi ({tournoi.nom}) : ") or tournoi.nom
            date_debut = input(f"Nouvelle date de début ({tournoi.date_debut}) : ") or tournoi.date_debut
            date_fin = input(f"Nouvelle date de fin ({tournoi.date_fin}) : ") or tournoi.date_fin
            nb_max_joueurs = input(f"Nouveau nombre maximal de joueurs ({tournoi.nb_max_joueurs}) : ") or tournoi.nb_max_joueurs
            nb_rondes = input(f"Nouveau nombre de rondes ({tournoi.nb_rondes}) : ") or tournoi.nb_rondes
            type_tournoi = input(f"Nouveau type de tournoi ({tournoi.type_tournoi}) : ") or tournoi.type_tournoi
            
            print("Modifications proposées :")
            print(f"Nom du tournoi : {nom}")
            print(f"Date de début : {date_debut}")
            print(f"Date de fin : {date_fin}")
            print(f"Nombre maximal de joueurs : {nb_max_joueurs}")
            print(f"Nombre de rondes : {nb_rondes}")
            print(f"Type de tournoi : {type_tournoi}")
            
            confirmation = input("Confirmez-vous ces modifications ? (o/n) : ")  # Demande de confirmation pour les modifications
            
            if confirmation.lower() == 'o':
                # Appel de la méthode pour modifier le tournoi avec les nouvelles informations
                self.tournoi_controller.modifier_tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
                print("Tournoi modifié avec succès.")
            else:
                print("Modification annulée.")
        else:
            print("Aucune modification effectuée.")

    # Méthode pour saisir l'index d'un tournoi
    def saisir_index_tournoi(self) -> Optional[int]:
        tournois = self.tournoi_controller.obtenir_liste_tournois()  # Obtention de la liste des tournois
        
        if not tournois:  # Vérification si des tournois sont disponibles
            print("Aucun tournoi disponible.")
            return None
        
        print("===== Liste des tournois =====")
        for i, tournoi in enumerate(tournois, 1):  # Affichage de la liste des tournois avec leur index
            if tournoi:
                print(f"{i}. {tournoi.nom} ({tournoi.date_debut} - {tournoi.date_fin})")
            else:
                print(f"{i}. Tournoi non trouvé")
        
        while True:
            try:
                choix = int(input("Entrez l'index du tournoi : "))  # Saisie de l'index du tournoi
                if 1 <= choix <= len(tournois):
                    return tournois[choix - 1].index  # Retourne l'index du tournoi sélectionné
                else:
                    print("Index invalide. Veuillez réessayer.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    # Méthode pour saisir les joueurs participants à un tournoi
    def saisir_joueurs_participants(self, index_tournoi: int) -> None:
        try:
            with open('data/joueur.json', 'r', encoding='utf-8') as f:  # Ouverture du fichier JSON contenant les joueurs
                tous_joueurs = json.load(f)  # Chargement des données des joueurs
        except FileNotFoundError:
            print("Fichier data/joueur.json non trouvé.")
            return
        except json.JSONDecodeError:
            print("Erreur dans le format du fichier data/joueur.json.")
            return
        
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        
        if not tournoi:  # Vérification si le tournoi existe
            print('Tournoi non trouvé.')
            return
        
        print(f'Joueurs actuellement inscrits dans le tournoi {tournoi.nom}:')
        for joueur in tournoi.joueurs:  # Affichage des joueurs déjà inscrits dans le tournoi
            print(f'- {joueur.nom} {joueur.prenom}')
        
        joueurs_inscrits_indices = [j.index for j in tournoi.joueurs]  # Liste des indices des joueurs inscrits
        joueurs_disponibles = [j for j in tous_joueurs if j['index'] not in joueurs_inscrits_indices]  # Liste des joueurs disponibles pour l'ajout
        
        if not joueurs_disponibles:  # Vérification si des joueurs sont disponibles pour l'ajout
            print("Aucun joueur disponible pour l'ajout.")
            return
        
        print('\nJoueurs disponibles:')
        for joueur in joueurs_disponibles:  # Affichage des joueurs disponibles
            print(f"{joueur['index']}. {joueur['nom']} {joueur['prenom']}")
        
        joueurs_selectionnes = []  # Liste des joueurs sélectionnés
        
        while len(tournoi.joueurs) + len(joueurs_selectionnes) < tournoi.nb_max_joueurs:
            try:
                choix = int(input('Entrez l\'index du joueur à ajouter (ou 0 pour terminer): '))  # Saisie de l'index du joueur à ajouter
                if choix == 0:
                    break
                
                joueur = next((j for j in joueurs_disponibles if j['index'] == choix), None)  # Recherche du joueur par index
                if joueur and joueur not in joueurs_selectionnes:
                    joueurs_selectionnes.append(joueur)  # Ajout du joueur à la liste des sélectionnés
                    print(f"Joueur {joueur['nom']} {joueur['prenom']} ajouté.")
                    joueurs_disponibles.remove(joueur)  # Retrait du joueur de la liste des disponibles
                else:
                    print('Index invalide ou joueur déjà inscrit.')
            except ValueError:
                print('Veuillez entrer un nombre valide.')
        
        if joueurs_selectionnes:  # Vérification si des joueurs ont été sélectionnés
            for joueur in joueurs_selectionnes:
                # Création d'un nouvel objet Joueur à partir des données du joueur sélectionné
                nouveau_joueur = Joueur(
                    index=joueur['index'],
                    nom=joueur['nom'],
                    prenom=joueur['prenom'],
                    date_naissance=datetime.date.fromisoformat(joueur['date_naissance']),
                    elo=joueur['elo']
                )
                tournoi.ajouter_joueur(nouveau_joueur)  # Ajout du joueur au tournoi
            tournoi.sauvegarder_joueurs()  # Sauvegarde des joueurs du tournoi
            print('Joueurs ajoutés au tournoi avec succès.')
        else:
            print('Aucun joueur n\'a été ajouté au tournoi.')

    # Méthode pour afficher la liste des tournois
    def afficher_liste_tournois(self):
        print("===== Liste des tournois =====")
        for i, tournoi in enumerate(self.tournoi_controller.tournoi_manager.tournois, 1):  # Affichage de la liste des tournois
            print(f"{i}. {tournoi.nom} ({tournoi.date_debut} - {tournoi.date_fin})")
        input("\nAppuyez sur Entrée pour revenir au menu principal...")

    # Méthode pour afficher les détails d'un tournoi
    def afficher_details_tournoi(self, index):
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index)  # Recherche du tournoi par index
        
        if not tournoi:  # Vérification si le tournoi existe
            print("Tournoi non trouvé.")
            return None
        
        print(f"===== Détails du tournoi {tournoi.nom} =====")
        print(f"Date de début : {tournoi.date_debut}")
        print(f"Date de fin : {tournoi.date_fin}")
        print(f"Nombre maximal de joueurs : {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes : {tournoi.nb_rondes}")
        print(f"Type de tournoi : {tournoi.type_tournoi}")
        print(f"Joueurs inscrits ({len(tournoi.joueurs)}):")
        for joueur in tournoi.joueurs:  # Affichage des joueurs inscrits
            print(f"- {joueur.nom} {joueur.prenom}")
        print("Rondes :")
        for ronde in tournoi.rondes:  # Affichage des rondes du tournoi
            print(f"Ronde {ronde.numero} :")
            for match in ronde.matchs:  # Affichage des matchs de chaque ronde
                print(f"- {match.joueur_blanc.nom} {match.joueur_blanc.prenom} vs {match.joueur_noir.nom} {match.joueur_noir.prenom} : {match.resultat}")
            print(f"Classement après la ronde {ronde.numero} :")
            for ligne in ronde.obtenir_classement_ronde():  # Affichage du classement après chaque ronde
                print(ligne)
        return tournoi

    # Méthode pour créer une nouvelle ronde dans un tournoi
    def creer_ronde(self, index_tournoi):
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        
        if not tournoi:  # Vérification si le tournoi existe
            print('Tournoi non trouvé.')
            return
        
        tournoi.jouer_ronde()  # Appel de la méthode pour jouer une nouvelle ronde
        self.tournoi_controller.tournoi_manager.sauvegarder_tournois()  # Sauvegarde des modifications des tournois
        print("Ronde créée avec succès.")

    # Méthode pour supprimer un joueur d'un tournoi
    def supprimer_joueur_tournoi(self, index_tournoi: int):
        tournoi = self.tournoi_controller.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        
        if not tournoi:  # Vérification si le tournoi existe
            print("Tournoi non trouvé.")
            return
        
        if not tournoi.joueurs:  # Vérification si des joueurs sont inscrits au tournoi
            print("Aucun joueur n'est inscrit à ce tournoi.")
            return
        
        print(f"Joueurs inscrits au tournoi {tournoi.nom}:")
        for i, joueur in enumerate(tournoi.joueurs, 1):  # Affichage des joueurs inscrits
            print(f"{i}. {joueur.nom} {joueur.prenom}")
        
        while True:
            try:
                choix = int(input("Entrez le numéro du joueur à supprimer (0 pour annuler) : "))  # Saisie du numéro du joueur à supprimer
                if choix == 0:
                    print("Suppression annulée.")
                    return
                
                if 1 <= choix <= len(tournoi.joueurs):
                    joueur_a_supprimer = tournoi.joueurs[choix - 1]  # Sélection du joueur à supprimer
                    if self.tournoi_controller.supprimer_joueur_du_tournoi(index_tournoi, joueur_a_supprimer):
                        print(f"Le joueur {joueur_a_supprimer.nom} {joueur_a_supprimer.prenom} a été supprimé du tournoi.")
                    else:
                        print("Erreur lors de la suppression du joueur.")
                    return
                else:
                    print("Numéro de joueur invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
