# Importation de la classe JoueurManager depuis le module models.joueur_model
from models.joueur_model import JoueurManager

# Importation du type Optional depuis le module typing
from typing import Optional

# Importation du module datetime pour gérer les dates
import datetime


# Définition de la classe JoueurController pour gérer les opérations sur les joueurs
class JoueurController:
    # Constructeur de la classe JoueurController
    def __init__(self):
        # Création d'une instance de JoueurManager pour gérer les données des joueurs
        self.joueur_manager = JoueurManager()

    # Méthode pour ajouter un joueur
    # Prend en paramètres le nom, le prénom, la date de naissance et l'elo du joueur
    # Retourne un booléen indiquant si l'ajout a réussi
    def ajouter_joueur(self, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> bool:
        # Appelle la méthode ajouter_joueur de JoueurManager avec les paramètres fournis
        return self.joueur_manager.ajouter_joueur(nom, prenom, date_naissance, elo)

    # Méthode pour modifier un joueur existant
    # Prend en paramètres l'index du joueur, le nom, le prénom, la date de naissance et l'elo
    # Ne retourne rien
    def modifier_joueur(self, index: int, nom: str, prenom: str, date_naissance: datetime.date, elo: int) -> None:
        # Appelle la méthode modifier_joueur de JoueurManager avec les paramètres fournis
        self.joueur_manager.modifier_joueur(index, nom, prenom, date_naissance, elo)
        # Affiche un message de succès
        print("Joueur modifié avec succès.")

    # Méthode pour supprimer un joueur
    # Prend en paramètre l'index du joueur
    # Ne retourne rien
    def supprimer_joueur(self, index: int) -> None:
        # Appelle la méthode supprimer_joueur de JoueurManager avec l'index fourni
        self.joueur_manager.supprimer_joueur(index)
        # Affiche un message de succès
        print("Joueur supprimé avec succès.")

    # Méthode pour obtenir la liste des joueurs
    # Retourne la liste des joueurs gérée par JoueurManager
    def obtenir_liste_joueurs(self):
        return self.joueur_manager.joueurs

    # Méthode pour obtenir un joueur par son index
    # Prend en paramètre l'index du joueur
    # Retourne le joueur si l'index est valide, sinon retourne None
    def obtenir_joueur_par_index(self, index: int):
        # Vérifie si l'index est valide (entre 1 et le nombre de joueurs)
        if 0 < index <= len(self.joueur_manager.joueurs):
            # Retourne le joueur correspondant à l'index (en ajustant pour l'indexation 0-based)
            return self.joueur_manager.joueurs[index - 1]
        # Retourne None si l'index est invalide
        return None

    # Méthode pour rechercher un joueur par son nom et prénom
    # Prend en paramètres le nom et le prénom du joueur
    # Retourne une liste des joueurs correspondant ou None si aucun joueur n'est trouvé
    def rechercher_joueur(self, nom: str, prenom: str) -> Optional[list]:
        # Utilise une liste en compréhension pour trouver les joueurs correspondant au nom et prénom
        return [joueur for joueur in self.joueur_manager.joueurs if joueur.nom == nom and joueur.prenom == prenom]