# Importation des modules nécessaires
import datetime  # Pour manipuler les dates
from models.tournoi_manager import TournoiManager  # Importation de la classe TournoiManager depuis le module models.tournoi_manager
from models.joueur_model import Joueur  # Importation de la classe Joueur depuis le module models.joueur_model
from typing import Optional  # Pour les annotations de type optionnelles

# Définition de la classe TournoiController pour gérer les opérations sur les tournois
class TournoiController:
    # Constructeur de la classe TournoiController
    def __init__(self):
        self.tournoi_manager = TournoiManager()  # Création d'une instance de TournoiManager

    # Méthode pour ajouter un tournoi
    def ajouter_tournoi(self, nom: str, date_debut: datetime.date, date_fin: datetime.date, nb_max_joueurs: int, nb_rondes: int, type_tournoi: str) -> bool:
        try:
            # Appelle la méthode ajouter_tournoi de TournoiManager avec les paramètres fournis
            return self.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
        except Exception as e:
            print(f"Erreur lors de l'ajout du tournoi : {str(e)}")  # Affiche un message d'erreur en cas d'exception
            return False  # Retourne False en cas d'échec

    # Méthode pour modifier un tournoi existant
    def modifier_tournoi(self, index: int, nom: str, date_debut: datetime.date, date_fin: datetime.date, nb_max_joueurs: int, nb_rondes: int, type_tournoi: str) -> None:
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            # Mise à jour des attributs du tournoi
            tournoi.nom = nom
            tournoi.date_debut = date_debut
            tournoi.date_fin = date_fin
            tournoi.nb_max_joueurs = nb_max_joueurs
            tournoi.nb_rondes = nb_rondes
            tournoi.type_tournoi = type_tournoi
            tournoi.sauvegarder_tournoi()  # Sauvegarde des modifications du tournoi
            print("Tournoi modifié avec succès.")  # Affiche un message de succès
        else:
            print("Tournoi non trouvé.")  # Affiche un message d'erreur si le tournoi n'est pas trouvé

    # Méthode pour supprimer un tournoi
    def supprimer_tournoi(self, index: int) -> None:
        self.tournoi_manager.supprimer_tournoi(index)  # Appelle la méthode supprimer_tournoi de TournoiManager

    # Méthode pour ajouter un joueur à un tournoi
    def ajouter_joueur_au_tournoi(self, index_tournoi: int, joueur: dict) -> bool:
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            # Création d'un nouvel objet Joueur à partir des données du dictionnaire joueur
            nouveau_joueur = Joueur(
                index=joueur['index'],
                nom=joueur['nom'],
                prenom=joueur['prenom'],
                date_naissance=datetime.datetime.strptime(joueur['date_naissance'], '%Y-%m-%d').date(),
                elo=joueur['elo']
            )
            if tournoi.ajouter_joueur(nouveau_joueur):  # Ajoute le joueur au tournoi
                tournoi.sauvegarder_tournoi()  # Sauvegarde des modifications du tournoi
                return True  # Retourne True en cas de succès
        return False  # Retourne False en cas d'échec

    # Méthode pour supprimer un joueur d'un tournoi
    def supprimer_joueur_du_tournoi(self, index_tournoi: int, joueur: Joueur) -> bool:
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            tournoi.joueurs.remove(joueur)  # Supprime le joueur de la liste des joueurs du tournoi
            tournoi.sauvegarder_joueurs()  # Sauvegarde des modifications des joueurs du tournoi
            tournoi.sauvegarder_tournoi()  # Sauvegarde des modifications du tournoi
            return True  # Retourne True en cas de succès
        return False  # Retourne False en cas d'échec

    # Méthode pour obtenir la liste des tournois
    def obtenir_liste_tournois(self):
        return self.tournoi_manager.tournois  # Retourne la liste des tournois gérés par TournoiManager

    # Méthode pour créer une nouvelle ronde dans un tournoi
    def creer_ronde(self, index_tournoi):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            tournoi.creer_ronde()  # Crée une nouvelle ronde
            self.tournoi_manager.sauvegarder_tournois()  # Sauvegarde des modifications des tournois
            print("Ronde créée avec succès.")  # Affiche un message de succès
        else:
            print("Tournoi non trouvé.")  # Affiche un message d'erreur si le tournoi n'est pas trouvé

    # Méthode pour modifier une ronde existante
    def modifier_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):  # Si le tournoi et la ronde sont trouvés
            ronde = tournoi.rondes[ronde_numero - 1]  # Sélectionne la ronde à modifier
            print(f"Modification de la ronde {ronde.numero}")

            for i, match in enumerate(ronde.matchs):  # Affiche les détails des matchs de la ronde
                print(f"Match {i + 1}: {match.joueur_blanc.nom} vs {match.joueur_noir.nom} - Résultat actuel: {match.resultat}")
                resultat = input(f"Entrez le nouveau résultat pour {match.joueur_blanc.nom} vs {match.joueur_noir.nom} (ex: 1-0, 0.5-0.5) ou laissez vide pour conserver l'actuel: ")
                if resultat:
                    match.saisir_resultat(resultat)  # Modifie le résultat du match

            self.tournoi_manager.sauvegarder_tournois()  # Sauvegarde des modifications des tournois
            print("Ronde modifiée avec succès.")  # Affiche un message de succès
        else:
            print("Numéro de ronde invalide.")  # Affiche un message d'erreur si la ronde n'est pas trouvée

    # Méthode pour supprimer une ronde existante
    def supprimer_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):  # Si le tournoi et la ronde sont trouvés
            tournoi.rondes.pop(ronde_numero - 1)  # Supprime la ronde de la liste des rondes du tournoi
            self.tournoi_manager.sauvegarder_tournois()  # Sauvegarde des modifications des tournois
            print("Ronde supprimée avec succès.")  # Affiche un message de succès
        else:
            print("Numéro de ronde invalide.")  # Affiche un message d'erreur si la ronde n'est pas trouvée

    # Méthode pour afficher les résultats d'une ronde
    def afficher_resultats_ronde(self, index_tournoi, ronde_numero):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi and 0 < ronde_numero <= len(tournoi.rondes):  # Si le tournoi et la ronde sont trouvés
            return tournoi.rondes[ronde_numero - 1]  # Retourne la ronde trouvée
        return None  # Retourne None si la ronde n'est pas trouvée

    # Méthode pour afficher le classement final d'un tournoi
    def afficher_classement_final(self, index_tournoi):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            scores = {}  # Dictionnaire pour stocker les scores des joueurs
            for ronde in tournoi.rondes:  # Parcourt toutes les rondes du tournoi
                for match in ronde.matchs:  # Parcourt tous les matchs de chaque ronde
                    joueur_blanc = match.joueur_blanc
                    joueur_noir = match.joueur_noir
                    resultat = match.resultat

                    if joueur_blanc not in scores:
                        scores[joueur_blanc] = 0
                    if joueur_noir not in scores:
                        scores[joueur_noir] = 0

                    if resultat == "1-0":
                        scores[joueur_blanc] += 1
                    elif resultat == "0-1":
                        scores[joueur_noir] += 1
                    elif resultat == "0.5-0.5":
                        scores[joueur_blanc] += 0.5
                        scores[joueur_noir] += 0.5

            classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)  # Trie les joueurs par score décroissant
            return classement  # Retourne le classement final
        else:
            print("Tournoi non trouvé")  # Affiche un message d'erreur si le tournoi n'est pas trouvé
            return None  # Retourne None en cas d'échec

    # Méthode pour trouver un tournoi par son index
    def trouver_tournoi_par_index(self, index):
        return self.tournoi_manager.trouver_tournoi_par_index(index)  # Appelle la méthode trouver_tournoi_par_index de TournoiManager

    # Méthode pour gérer l'appariement des rondes d'un tournoi
    def appariement_ronde(self, index_tournoi):
        self.tournoi_manager.appariement_ronde(index_tournoi)  # Appelle la méthode appariement_ronde de TournoiManager

    # Méthode pour obtenir les résultats d'une ronde
    def obtenir_resultats_ronde(self, index_tournoi):
        return self.tournoi_manager.obtenir_resultats_ronde(index_tournoi)  # Appelle la méthode obtenir_resultats_ronde de TournoiManager

    # Méthode pour obtenir le classement d'une ronde
    def obtenir_classement_ronde(self, index_tournoi):
        return self.tournoi_manager.obtenir_classement_ronde(index_tournoi)  # Appelle la méthode obtenir_classement_ronde de TournoiManager
