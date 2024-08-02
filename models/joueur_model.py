# Importation des modules nécessaires
import json  # Pour manipuler les fichiers JSON
import os  # Pour les opérations liées au système de fichiers
import datetime  # Pour manipuler les dates
from typing import Optional, List, Dict  # Pour les annotations de type


# Définition de la classe Joueur pour représenter un joueur
class Joueur:
    # Constructeur de la classe Joueur
    def __init__(self, index: int, nom: str, prenom: str, date_naissance: datetime.date, elo: int):
        self.index = index  # Index du joueur
        self.nom = nom  # Nom du joueur
        self.prenom = prenom  # Prénom du joueur
        self.date_naissance = date_naissance  # Date de naissance du joueur
        self.elo = elo  # Classement Elo du joueur
        self.score = 0  # Initialiser le score à 0

    # Méthode pour convertir un objet Joueur en dictionnaire
    def to_dict(self) -> Dict:
        return {
            'index': self.index,
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance.isoformat(),  # Convertir la date en chaîne ISO
            'elo': self.elo,
            'score': self.score
        }

    # Méthode de classe pour créer un objet Joueur à partir d'un dictionnaire
    @classmethod
    def from_dict(cls, data: Dict) -> 'Joueur':
        return cls(
            index=data['index'],
            nom=data['nom'],
            prenom=data['prenom'],
            date_naissance=datetime.date.fromisoformat(data['date_naissance']),  # Convertir la date ISO en objet date
            elo=data['elo']
        )

    # Méthode pour comparer deux objets Joueur
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Joueur):
            return NotImplemented
        return self.index == other.index  # Comparer les index

    # Méthode pour représenter un objet Joueur sous forme de chaîne
    def __str__(self) -> str:
        return f"{self.prenom} {self.nom} ({self.date_naissance}) - Elo: {self.elo}"

    # Méthode pour obtenir le hash d'un objet Joueur
    def __hash__(self):
        return hash(self.index)


# Définition de la classe JoueurManager pour gérer les opérations sur les joueurs
class JoueurManager:
    MAX_JOUEURS = 100  # Nombre maximum de joueurs
    FICHIER_JSON = "data/joueur.json"  # Chemin du fichier JSON

    # Constructeur de la classe JoueurManager
    def __init__(self):
        self.joueurs: List[Joueur] = []  # Liste des joueurs
        self.charger_joueurs()  # Charger les joueurs depuis le fichier JSON

    # Méthode pour charger les joueurs depuis le fichier JSON
    def charger_joueurs(self) -> List[Joueur]:
        try:
            with open(self.FICHIER_JSON, 'r', encoding='utf-8') as f:
                joueurs_data = json.load(f)  # Charger les données JSON
            self.joueurs = [Joueur.from_dict(joueur_data) for joueur_data in joueurs_data]  # Convertir les dictionnaires en objets Joueur
        except FileNotFoundError:
            print("Fichier data/joueur.json non trouvé. Création d'une nouvelle liste de joueurs.")
        except json.JSONDecodeError:
            print("Erreur dans le format du fichier data/joueur.json. Création d'une nouvelle liste de joueurs.")

    # Méthode pour sauvegarder les joueurs dans le fichier JSON
    def sauvegarder_joueurs(self) -> None:
        with open(self.FICHIER_JSON, "w", encoding='utf-8') as file:
            data = [joueur.to_dict() for joueur in self.joueurs]  # Convertir les objets Joueur en dictionnaires
            json.dump(data, file, indent=4)  # Sauvegarder les données JSON

    # Méthode pour ajouter un joueur
    def ajouter_joueur(self, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> bool:
        joueur_existant = self.trouver_joueur_par_details(nom, prenom, date_naissance)  # Vérifier si le joueur existe déjà
        if joueur_existant:
            print("Ce joueur existe déjà.")
            return False

        age_minimum = datetime.timedelta(days=7 * 365)  # Définir l'âge minimum (7 ans)
        if (datetime.date.today() - date_naissance) < age_minimum:
            print("Le joueur doit avoir au moins 7 ans pour s'inscrire.")
            return False

        if len(self.joueurs) < self.MAX_JOUEURS:
            index = len(self.joueurs) + 1  # Définir l'index du nouveau joueur
            nouveau_joueur = Joueur(index, nom, prenom, date_naissance, elo)  # Créer un nouvel objet Joueur
            self.joueurs.append(nouveau_joueur)  # Ajouter le joueur à la liste
            self.sauvegarder_joueurs()  # Sauvegarder les modifications
            return True
        else:
            print("Nombre maximum de joueurs atteint.")
            return False

    # Méthode pour trouver un joueur par ses détails
    def trouver_joueur_par_details(self, nom: str, prenom: str, date_naissance: datetime.date) -> Optional[Joueur]:
        for joueur in self.joueurs:
            if joueur.nom == nom and joueur.prenom == prenom and joueur.date_naissance == date_naissance:
                return joueur
        return None

    # Méthode pour supprimer un joueur
    def supprimer_joueur(self, index: int) -> bool:
        joueur = self.trouver_joueur_par_index(index)
        if joueur:
            self.joueurs.remove(joueur)
            self.sauvegarder_joueurs()
            return True
        else:
            print("Joueur non trouvé.")
            return False

    # Méthode pour trouver un joueur par son index
    def trouver_joueur_par_index(self, index: int) -> Optional[Joueur]:
        for joueur in self.joueurs:
            if joueur.index == index:
                return joueur
        return None