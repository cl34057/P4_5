# Importation des modules nécessaires
import datetime  # Pour manipuler les dates
import json  # Pour manipuler les fichiers JSON
import os  # Pour les opérations liées au système de fichiers
from typing import List, Optional, Tuple  # Pour les annotations de type

# Importation des classes nécessaires depuis les modules correspondants
from models.tournoi_model import Tournoi  # Modèle pour les tournois
from models.joueur_model import Joueur  # Modèle pour les joueurs

# Définition de la classe TournoiManager pour gérer les opérations sur les tournois
class TournoiManager:
    MAX_TOURNOIS = 30  # Nombre maximum de tournois
    FICHIER_JSON = "data/tournaments.json"  # Chemin du fichier JSON

    # Constructeur de la classe TournoiManager
    def __init__(self):
        self.tournois: List[Tournoi] = []  # Liste des tournois
        self.charger_tournois()  # Charger les tournois depuis le fichier JSON

    # Méthode pour charger les tournois depuis un fichier JSON
    def charger_tournois(self) -> None:
        if os.path.exists(self.FICHIER_JSON):  # Vérifie si le fichier JSON existe
            with open(self.FICHIER_JSON, "r", encoding='utf-8') as file:  # Ouvre le fichier en lecture
                try:
                    data = json.load(file)  # Charge les données JSON
                    self.tournois = [Tournoi.from_dict(tournoi_data) for tournoi_data in data.values()]  # Convertit les dictionnaires en objets Tournoi
                    self.reindexer_tournois()  # Réindexe les tournois
                except json.JSONDecodeError as e:
                    print(f"Erreur lors du chargement des tournois: {str(e)}")  # Affiche un message d'erreur en cas d'exception

    # Méthode pour charger un tournoi spécifique depuis un fichier JSON
    def charger_tournoi(nom_tournoi):
        with open(f'data/tournaments/{nom_tournoi}.json', 'r') as f:  # Ouvre le fichier spécifique en lecture
            tournoi_data = json.load(f)  # Charge les données JSON
            tournoi = Tournoi(
                index=tournoi_data['index'],
                nom=tournoi_data['nom'],
                date_debut=datetime.fromisoformat(tournoi_data['date_debut']).date(),
                date_fin=datetime.fromisoformat(tournoi_data['date_fin']).date(),
                nb_max_joueurs=tournoi_data['nb_max_joueurs'],
                nb_rondes=tournoi_data['nb_rondes'],
                type_tournoi=tournoi_data['type_tournoi']
            )
            tournoi.joueurs = [Joueur(nom) for nom in tournoi_data['joueurs']]  # Convertit les noms de joueurs en objets Joueur
            for ronde_data in tournoi_data['rondes']:  # Parcourt les rondes du tournoi
                ronde = Ronde(
                    numero=ronde_data['numero'],
                    date=datetime.fromisoformat(ronde_data['date']),
                    statut=ronde_data['statut']
                )
                for match_data in ronde_data['matchs']:  # Parcourt les matchs de chaque ronde
                    joueur_blanc_nom, joueur_noir_nom = match_data['match'].split(' - ')
                    joueur_blanc = next(j for j in tournoi.joueurs if j.nom == joueur_blanc_nom.strip())
                    joueur_noir = next(j for j in tournoi.joueurs if j.nom == joueur_noir_nom.strip())
                    match = Match(joueur_blanc, joueur_noir, match_data['score'])
                    ronde.matchs.append(match)
                ronde.classement_apres_ronde = ronde_data['classement_apres_ronde']
                tournoi.rondes.append(ronde)
            return tournoi

    # Méthode pour sauvegarder les tournois dans un fichier JSON
    def sauvegarder_tournois(self) -> None:
        data = {tournoi.nom: tournoi.to_dict_base() for tournoi in self.tournois}  # Convertit les objets Tournoi en dictionnaires
        with open(self.FICHIER_JSON, "w", encoding='utf-8') as file:  # Ouvre le fichier en écriture
            json.dump(data, file, indent=4, ensure_ascii=False)  # Écrit les données JSON dans le fichier

    # Méthode pour trouver un tournoi par son index
    def trouver_tournoi_par_index(self, index: int) -> Optional[Tournoi]:
        for tournoi in self.tournois:  # Parcourt tous les tournois
            if tournoi.index == index:  # Si l'index correspond
                return tournoi  # Retourne le tournoi trouvé
        return None  # Retourne None si aucun tournoi n'est trouvé

    # Méthode pour ajouter un nouveau tournoi
    def ajouter_tournoi(self, nom: str, date_debut: datetime.date, date_fin: datetime.date, nb_max_joueurs: int, nb_rondes: int, type_tournoi: str) -> Optional[Tournoi]:
        if len(self.tournois) >= self.MAX_TOURNOIS:  # Vérifie si le nombre maximum de tournois est atteint
            print("Nombre maximum de tournois atteint.")
            return None
        try:
            index = max((tournoi.index for tournoi in self.tournois), default=0) + 1  # Détermine le nouvel index
            nouveau_tournoi = Tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)  # Crée un nouvel objet Tournoi
            self.tournois.append(nouveau_tournoi)  # Ajoute le nouveau tournoi à la liste
            self.sauvegarder_tournois()  # Sauvegarde les tournois
            print(f"Tournoi '{nom}' ajouté avec succès.")
            return nouveau_tournoi
        except Exception as e:
            print(f"Erreur lors de l'ajout du tournoi : {str(e)}")  # Affiche un message d'erreur en cas d'exception
            return None

    # Méthode pour supprimer un tournoi par son index
    def supprimer_tournoi(self, index_tournoi: int) -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            self.tournois.remove(tournoi)  # Supprime le tournoi de la liste
            fichier_tournoi = f"data/tournaments/{tournoi.nom.replace(' ', '_')}.json"  # Chemin du fichier du tournoi
            if os.path.exists(fichier_tournoi):  # Vérifie si le fichier existe
                os.remove(fichier_tournoi)  # Supprime le fichier
            fichier_joueurs = f"data/tournaments/{tournoi.nom.replace(' ', '_')}_joueurs.json"  # Chemin du fichier des joueurs
            if os.path.exists(fichier_joueurs):  # Vérifie si le fichier existe
                os.remove(fichier_joueurs)  # Supprime le fichier
            self.reindexer_tournois()  # Réindexe les tournois
            self.sauvegarder_tournois()  # Sauvegarde les tournois
            print("Tournoi supprimé avec succès.")
            return True
        else:
            print(f"Erreur : Tournoi avec l'index {index_tournoi} non trouvé.")
            return False

    # Méthode pour réindexer les tournois
    def reindexer_tournois(self) -> None:
        for i, tournoi in enumerate(self.tournois):  # Parcourt tous les tournois
            if tournoi is not None:
                tournoi.index = i  # Réindexe le tournoi
            else:
                print("Warning: Un tournoi est None. Ignorer.")  # Affiche un avertissement si un tournoi est None

    # Méthode pour ajouter un joueur à un tournoi
    def ajouter_joueur_au_tournoi(self, index_tournoi: int, joueur: dict) -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            nouveau_joueur = Joueur(
                index=joueur['index'],
                nom=joueur['nom'],
                prenom=joueur['prenom'],
                date_naissance=datetime.datetime.strptime(joueur['date_naissance'], '%Y-%m-%d').date(),
                elo=joueur['elo']
            )
            if tournoi.ajouter_joueur(nouveau_joueur):  # Ajoute le joueur au tournoi
                self.sauvegarder_tournois()  # Sauvegarde les tournois
                return True
        return False

    # Méthode pour supprimer un joueur d'un tournoi
    def supprimer_joueur_tournoi(self, index_tournoi: int, joueur: Joueur) -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi:  # Si le tournoi est trouvé
            return tournoi.supprimer_joueur(joueur)  # Supprime le joueur du tournoi
        return False

    # Méthode pour créer une nouvelle ronde pour un tournoi
    def creer_ronde(self, index_tournoi: int) -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if tournoi and tournoi.creer_ronde():  # Si le tournoi est trouvé et la ronde est créée
            self.sauvegarder_tournois()  # Sauvegarde les tournois
            return True
        return False

    # Méthode pour obtenir le classement final d'un tournoi
    def obtenir_classement_tournoi(self, index_tournoi: int) -> List[Tuple[Joueur, float]]:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        return tournoi.classement() if tournoi else []  # Retourne le classement du tournoi ou une liste vide

    # Méthode pour exporter les données d'un tournoi
    def exporter_tournoi(self, index_tournoi: int, format: str = 'json') -> bool:
        tournoi = self.trouver_tournoi_par_index(index_tournoi)  # Recherche du tournoi par index
        if not tournoi:  # Si le tournoi n'est pas trouvé
            return False
        if format == 'json':  # Si le format est JSON
            fichier = f"exports/{tournoi.nom}_export.json"  # Chemin du fichier d'export
            with open(fichier, 'w', encoding='utf-8') as file:  # Ouvre le fichier en écriture
                json.dump(tournoi.to_dict(), file, indent=4, ensure_ascii=False)  # Écrit les données JSON dans le fichier
            return True
        else:
            print(f"Format d'export '{format}' non supporté.")  # Affiche un message d'erreur pour format non supporté
            return False

    # Méthode pour importer un tournoi depuis un fichier JSON
    def importer_tournoi(self, fichier: str) -> Optional[Tournoi]:
        if not os.path.exists(fichier):  # Vérifie si le fichier existe
            print(f"Le fichier {fichier} n'existe pas.")
            return None
        try:
            with open(fichier, 'r', encoding='utf-8') as file:  # Ouvre le fichier en lecture
                data = json.load(file)  # Charge les données JSON
                nouveau_tournoi = Tournoi(
                    len(self.tournois) + 1,
                    data.get('nom_tournoi', 'Tournoi sans nom'),
                    datetime.datetime.fromisoformat(data.get('date_debut', '2000-01-01')).date(),
                    datetime.datetime.fromisoformat(data.get('date_fin', '2000-01-02')).date(),
                    int(data.get('nb_max_joueurs', 0)),
                    int(data.get('nb_rondes', 0)),
                    data.get('type_tournoi', 'Type inconnu')
                )
                self.tournois.append(nouveau_tournoi)  # Ajoute le nouveau tournoi à la liste
                self.sauvegarder_tournois()  # Sauvegarde les tournois
                return nouveau_tournoi
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erreur lors de l'importation du tournoi : {str(e)}")  # Affiche un message d'erreur en cas d'exception
            return None
