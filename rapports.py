# Importation des modules nécessaires
from typing import List  # Pour les annotations de type de liste
from models.joueur_model import Joueur  # Importation de la classe Joueur depuis le module joueur_model
from models.tournoi_model import Tournoi  # Importation de la classe Tournoi depuis le module tournoi_model


# Fonction pour générer une liste de joueurs triée par ordre alphabétique
def liste_joueurs_alphabetique(joueurs: List[Joueur]) -> str:
    # Trie les joueurs par nom et prénom
    joueurs_triees = sorted(joueurs, key=lambda joueur: (joueur.nom, joueur.prenom))
    # Initialise le rapport avec un titre
    rapport = "Liste de tous les joueurs par ordre alphabétique:\n"
    # Ajoute chaque joueur trié au rapport
    rapport += "\n".join(f"{joueur.nom} {joueur.prenom}" for joueur in joueurs_triees)
    return rapport  # Retourne le rapport


# Fonction pour générer une liste de tournois
def liste_tournois(tournois: List[Tournoi]) -> str:
    # Initialise le rapport avec un titre
    rapport = "Liste de tous les tournois:\n"
    # Ajoute chaque tournoi au rapport
    rapport += "\n".join(tournoi.nom for tournoi in tournois)
    return rapport  # Retourne le rapport


# Fonction pour générer les détails d'un tournoi
def details_tournoi(tournoi: Tournoi) -> str:
    # Initialise le rapport avec les détails du tournoi
    rapport = f"Nom du tournoi: {tournoi.nom}\n"
    rapport += f"Date de début: {tournoi.date_debut}\n"
    rapport += f"Date de fin: {tournoi.date_fin}\n"
    return rapport  # Retourne le rapport


# Fonction pour générer une liste de joueurs d'un tournoi triée par ordre alphabétique
def liste_joueurs_tournoi_alphabetique(tournoi: Tournoi) -> str:
    # Utilise la fonction liste_joueurs_alphabetique pour trier les joueurs du tournoi
    return liste_joueurs_alphabetique(tournoi.joueurs)


# Fonction pour générer la liste des tours et des matchs d'un tournoi
def liste_tours_et_matchs(tournoi: Tournoi) -> str:
    # Initialise le résultat avec un titre
    resultat = f"Tours et matchs du tournoi {tournoi.nom}:\n\n"

    # Vérifie si des rondes ont été jouées
    if not tournoi.rondes:
        return resultat + "Aucune ronde n'a été jouée dans ce tournoi.\n"

    # Parcourt chaque ronde du tournoi
    for ronde in tournoi.rondes:
        resultat += f"Ronde {ronde.numero} ({ronde.statut}):\n"
        # Vérifie si des matchs ont été joués dans la ronde
        if ronde.matchs:
            for match in ronde.matchs:
                resultat += f" {match.joueur_blanc.nom} vs {match.joueur_noir.nom} : {match.resultat or 'Non joué'}\n"
        else:
            resultat += " Aucun match n'a été joué dans cette ronde.\n"
        resultat += "\n"

        # Obtient le classement après la ronde
        classement = ronde.obtenir_classement_ronde()
        if classement:
            resultat += "Classement après la ronde:\n"
            for ligne in classement:
                resultat += f" {ligne}\n"
            resultat += "\n"

    return resultat  # Retourne le résultat


# Fonction alternative pour générer la liste des tours et des matchs d'un tournoi
def liste_tours_et_matchs_alternative(tournoi: Tournoi) -> str:
    resultat = ""  # Initialise le résultat
    # Parcourt chaque ronde du tournoi
    for ronde in tournoi.rondes:
        resultat += f"Ronde {ronde.numero} ({ronde.date} - {ronde.statut})\n"
        # Parcourt chaque match de la ronde
        for match in ronde.matchs:
            resultat += f"  Match : {match.joueur_blanc.nom} vs {match.joueur_noir.nom} - Score : {match.resultat}\n"
        resultat += "Classement après la ronde :\n"
        # Ajoute le classement après la ronde
        for classement in ronde.classement_apres_ronde:
            resultat += f"  {classement}\n"
    return resultat  # Retourne le résultat