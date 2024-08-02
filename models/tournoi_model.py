# Importation des modules nécessaires
import datetime  # Pour manipuler les dates
import json  # Pour manipuler les fichiers JSON
import os  # Pour les opérations liées au système de fichiers
import random  # Pour générer des nombres aléatoires
from typing import List, Dict, Tuple, Optional  # Pour les annotations de type
from models.joueur_model import Joueur  # Importation de la classe Joueur

# Définition de la classe Match
class Match:
    def __init__(self, joueur_blanc: Joueur, joueur_noir: Joueur, resultat: str = ""):
        self.joueur_blanc = joueur_blanc  # Joueur avec les pièces blanches
        self.joueur_noir = joueur_noir  # Joueur avec les pièces noires
        self.resultat = resultat  # Résultat du match (vide par défaut)

    def saisir_resultat(self, resultat: str) -> None:
        if resultat in ["1-0", "0-1", "0.5-0.5"]:  # Vérification du format du résultat
            self.resultat = resultat  # Enregistrement du résultat
        else:
            raise ValueError("Le résultat doit être '1-0', '0-1' ou '0.5-0.5'.")  # Erreur si format invalide

    def to_dict(self) -> Dict[str, str]:
        return {
            "match": f"{self.joueur_blanc.nom} {self.joueur_blanc.prenom} - {self.joueur_noir.nom} {self.joueur_noir.prenom}",
            "score": self.resultat if self.resultat else "Non joué"
        }

    def __repr__(self) -> str:
        return f"{self.joueur_blanc.nom} vs {self.joueur_noir.nom}: {self.resultat}"

# Définition de la classe Ronde
class Ronde:
    def __init__(self, numero: int, date: Optional[datetime.datetime] = None, statut: str = "en cours"):
        self.numero = numero  # Numéro de la ronde
        self.date = date if date else datetime.datetime.now()  # Date de la ronde (par défaut: maintenant)
        self.statut = statut  # Statut de la ronde
        self.matchs: List[Match] = []  # Liste des matchs de la ronde

    def ajouter_match(self, match: Match) -> None:
        self.matchs.append(match)  # Ajout d'un match à la ronde

    def terminer_ronde(self) -> None:
        self.date_fin = datetime.datetime.now()  # Enregistrement de la date de fin
        self.statut = "terminée"  # Changement du statut à "terminée"

    def to_dict(self) -> Dict:
        return {
            "numero": self.numero,
            "date": self.date.isoformat(),
            "statut": self.statut,
            "matchs": [match.to_dict() for match in self.matchs],
            "classement_apres_ronde": self.obtenir_classement_ronde()
        }

    def appariement_ronde(self, joueurs: List[Joueur]) -> None:
        if len(joueurs) < 2:
            print("Nombre insuffisant de joueurs pour créer des paires.")
            return
        random.shuffle(joueurs)  # Mélange aléatoire des joueurs
        paires = [(joueurs[i], joueurs[i + 1]) for i in range(0, len(joueurs), 2) if i + 1 < len(joueurs)]
        self.matchs = [Match(pair[0], pair[1]) for pair in paires]  # Création des matchs

    def obtenir_resultats_ronde(self) -> None:
        print(f"Obtention des résultats pour la ronde {self.numero}.")
        for match in self.matchs:
            print(f"Match entre {match.joueur_blanc.nom} et {match.joueur_noir.nom}: {match.resultat}")

    def obtenir_classement_ronde(self) -> List[str]:
        classement: Dict[Joueur, float] = {match.joueur_blanc: 0 for match in self.matchs}
        classement.update({match.joueur_noir: 0 for match in self.matchs})
        for match in self.matchs:
            if match.resultat == "1-0":
                classement[match.joueur_blanc] += 1
            elif match.resultat == "0-1":
                classement[match.joueur_noir] += 1
            elif match.resultat == "0.5-0.5":
                classement[match.joueur_blanc] += 0.5
                classement[match.joueur_noir] += 0.5
        classement = sorted(classement.items(), key=lambda item: item[1], reverse=True)
        return [f"{i + 1}. {joueur.nom} {joueur.prenom} : {points}" for i, (joueur, points) in enumerate(classement)]

# Définition de la classe Tournoi
class Tournoi:
    def __init__(self, index: int, nom: str, date_debut: datetime.date, date_fin: datetime.date, nb_max_joueurs: int,
                 nb_rondes: int, type_tournoi: str):
        self.index = index  # Index du tournoi
        self.nom = nom  # Nom du tournoi
        self.date_debut = date_debut  # Date de début du tournoi
        self.date_fin = date_fin  # Date de fin du tournoi
        self.nb_max_joueurs = nb_max_joueurs  # Nombre maximum de joueurs
        self.nb_rondes = nb_rondes  # Nombre de rondes
        self.type_tournoi = type_tournoi  # Type de tournoi
        self.joueurs: List[Joueur] = []  # Liste des joueurs
        self.rondes: List[Ronde] = []  # Liste des rondes
        self.statut = "En attente"  # Statut initial du tournoi
        self.charger_joueurs()  # Chargement des joueurs

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "nom_tournoi": self.nom,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat(),
            "nb_rondes": int(self.nb_rondes),
            "nb_inscrits": len(self.joueurs),
            "nb_max_joueurs": int(self.nb_max_joueurs),
            "type_tournoi": self.type_tournoi,
            "statut": self.statut,
            "joueurs_inscrits": [joueur.index for joueur in self.joueurs],
            "rondes": [ronde.to_dict() for ronde in self.rondes]
        }

    def to_dict_base(self) -> Dict:
        return {
            "index": self.index,
            "nom_tournoi": self.nom,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat(),
            "nb_rondes": int(self.nb_rondes),
            "nb_max_joueurs": int(self.nb_max_joueurs),
            "type_tournoi": self.type_tournoi
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Tournoi':
        tournoi = cls(
            data["index"],
            data["nom_tournoi"],
            datetime.date.fromisoformat(data["date_debut"]),
            datetime.date.fromisoformat(data["date_fin"]),
            data["nb_max_joueurs"],
            data["nb_rondes"],
            data["type_tournoi"]
        )
        tournoi.statut = data.get("statut", "En attente")
        tournoi.charger_joueurs()
        for ronde_data in data.get("rondes", []):
            ronde = Ronde(
                numero=ronde_data["numero"],
                date=datetime.datetime.fromisoformat(ronde_data["date"]),
                statut=ronde_data["statut"]
            )
            for match_data in ronde_data.get("matchs", []):
                joueur_blanc = next(
                    (j for j in tournoi.joueurs if f"{j.nom} {j.prenom}" == match_data["match"].split(" - ")[0].strip()),
                    None
                )
                joueur_noir = next(
                    (j for j in tournoi.joueurs if f"{j.nom} {j.prenom}" == match_data["match"].split(" - ")[1].strip()),
                    None
                )
                if joueur_blanc and joueur_noir:
                    match = Match(joueur_blanc, joueur_noir, match_data["score"])
                    ronde.ajouter_match(match)
            tournoi.rondes.append(ronde)
        return tournoi

    def ajouter_joueur(self, joueur: Joueur) -> bool:
        if len(self.joueurs) < self.nb_max_joueurs and joueur not in self.joueurs:
            self.joueurs.append(joueur)
            self.sauvegarder_joueurs()
            self.sauvegarder_tournoi()
            return True
        return False

    def creer_ronde(self) -> Optional[Ronde]:
        if len(self.rondes) >= self.nb_rondes:
            print(f"Impossible de créer une nouvelle ronde. Le nombre maximum de rondes ({self.nb_rondes}) a déjà été atteint.")
            return None
        if len(self.joueurs) < 8:
            print(f"Impossible de créer une ronde. Il y a actuellement {len(self.joueurs)} joueurs inscrits, mais un minimum de 8 joueurs est requis.")
            return None
        nouvelle_ronde = Ronde(len(self.rondes) + 1, datetime.datetime.now())
        joueurs_disponibles = self.joueurs.copy()
        random.shuffle(joueurs_disponibles)
        while len(joueurs_disponibles) >= 2:
            joueur1 = joueurs_disponibles.pop()
            joueur2 = joueurs_disponibles.pop()
            match = Match(joueur1, joueur2)
            nouvelle_ronde.ajouter_match(match)
        if joueurs_disponibles:
            print(f"Le joueur {joueurs_disponibles[0].nom} {joueurs_disponibles[0].prenom} reçoit un bye pour cette ronde.")
        self.rondes.append(nouvelle_ronde)
        print(f"Ronde {nouvelle_ronde.numero} créée avec succès.")
        for match in nouvelle_ronde.matchs:
            print(f"{match.joueur_blanc.nom} {match.joueur_blanc.prenom} - {match.joueur_noir.nom} {match.joueur_noir.prenom}")
        self.sauvegarder_tournoi()
        return nouvelle_ronde

    def charger_joueurs(self) -> None:
        fichier_joueurs = f"data/tournaments/{self.nom.replace(' ', '_')}_joueurs.json"
        if os.path.exists(fichier_joueurs):
            with open(fichier_joueurs, 'r', encoding='utf-8') as file:
                joueurs_data = json.load(file)
            self.joueurs = [Joueur.from_dict(joueur_data) for joueur_data in joueurs_data]
        else:
            print(f"Fichier {fichier_joueurs} non trouvé.")

    def generer_paires(self) -> List[Tuple[Joueur, Joueur]]:
        joueurs = set(self.joueurs)
        paires = []
        deja_apparies = set()
        while len(joueurs) >= 2:
            j1 = joueurs.pop()
            j2 = joueurs.pop()
            while (j1, j2) in deja_apparies or (j2, j1) in deja_apparies:
                joueurs.add(j1)
                j1 = joueurs.pop()
                joueurs.add(j2)
                j2 = joueurs.pop()
            paires.append((j1, j2))
            deja_apparies.add((j1, j2))
        return paires

    def jouer_ronde(self) -> None:
        if len(self.rondes) >= self.nb_rondes:
            print("Toutes les rondes ont été jouées.")
            return
        nouvelle_ronde = Ronde(len(self.rondes) + 1, datetime.datetime.now())
        paires = self.generer_paires()
        for j1, j2 in paires:
            match = Match(j1, j2)
            nouvelle_ronde.ajouter_match(match)
        self.rondes.append(nouvelle_ronde)
        print(f"Ronde {nouvelle_ronde.numero} créée avec succès.")
        for match in nouvelle_ronde.matchs:
            print(f"{match.joueur_blanc.nom} {match.joueur_blanc.prenom} - {match.joueur_noir.nom} {match.joueur_noir.prenom}")
        for match in nouvelle_ronde.matchs:
            while True:
                resultat = input(f"Résultat du match {match.joueur_blanc.nom} {match.joueur_blanc.prenom} vs {match.joueur_noir.nom} {match.joueur_noir.prenom} (1-0, 0-1, 0.5-0.5) : ")
                try:
                    match.saisir_resultat(resultat)
                    self.mettre_a_jour_scores_match(match, resultat)
                    break
                except ValueError as e:
                    print(e)
        nouvelle_ronde.statut = "terminée"
        print("\nClassement après la ronde :")
        for ligne in nouvelle_ronde.obtenir_classement_ronde():
            print(ligne)
        self.calculer_classement_cumulatif()
        self.sauvegarder_tournoi()
        print(f"Ronde {nouvelle_ronde.numero} terminée et sauvegardée.")

    def saisir_resultats_ronde(self, numero_ronde: int) -> None:
        if numero_ronde <= 0 or numero_ronde > len(self.rondes):
            print(f"Numéro de ronde invalide. Il y a {len(self.rondes)} rondes dans ce tournoi.")
            return
        ronde = self.rondes[numero_ronde - 1]
        print(f"Saisie des résultats pour la ronde {numero_ronde}")
        for match in ronde.matchs:
            while True:
                resultat = input(f"Résultat du match {match.joueur_blanc.nom} vs {match.joueur_noir.nom} (1-0, 0-1, 0.5-0.5) : ")
                try:
                    match.saisir_resultat(resultat)
                    self.mettre_a_jour_scores_match(match, resultat)
                    break
                except ValueError as e:
                    print(e)
        ronde.statut = "terminée"
        self.calculer_classement_cumulatif()
        print("\nClassement après la ronde :")
        for ligne in ronde.obtenir_classement_ronde():
            print(ligne)
        self.sauvegarder_tournoi()
        print(f"Résultats de la ronde {numero_ronde} saisis, classement mis à jour et sauvegardés.")

    def mettre_a_jour_scores_match(self, match: Match, resultat: str) -> None:
        if resultat == "1-0":
            match.joueur_blanc.score += 1
        elif resultat == "0-1":
            match.joueur_noir.score += 1
        elif resultat == "0.5-0.5":
            match.joueur_blanc.score += 0.5
            match.joueur_noir.score += 0.5

    def mettre_a_jour_scores(self) -> None:
        for joueur in self.joueurs:
            joueur.score = 0
        for ronde in self.rondes:
            for match in ronde.matchs:
                if match.resultat == "1-0":
                    match.joueur_blanc.score += 1
                elif match.resultat == "0-1":
                    match.joueur_noir.score += 1
                elif match.resultat == "0.5-0.5":
                    match.joueur_blanc.score += 0.5
                    match.joueur_noir.score += 0.5

    def classement(self) -> List[Tuple[Joueur, float]]:
        return sorted([(j, j.score) for j in self.joueurs], key=lambda x: x[1], reverse=True)

    def calculer_classement_cumulatif(self) -> None:
        points_cumules = {joueur.nom: 0 for joueur in self.joueurs}
        for ronde in self.rondes:
            for match in ronde.matchs:
                if match.resultat == "1-0":
                    points_cumules[match.joueur_blanc.nom] += 1
                elif match.resultat == "0-1":
                    points_cumules[match.joueur_noir.nom] += 1
                elif match.resultat == "0.5-0.5":
                    points_cumules[match.joueur_blanc.nom] += 0.5
                    points_cumules[match.joueur_noir.nom] += 0.5
        classement = sorted(points_cumules.items(), key=lambda item: item[1], reverse=True)
        for ronde in self.rondes:
            ronde.obtenir_classement_ronde = lambda: [f"{i + 1}. {joueur} : {points}" for i, (joueur, points) in enumerate(classement)]

    def sauvegarder_tournoi(self) -> None:
        fichier_tournoi = f"data/tournaments/{self.nom.replace(' ', '_')}.json"
        with open(fichier_tournoi, "w", encoding='utf-8') as file:
            json.dump(self.to_dict(), file, indent=4, ensure_ascii=False)

    def demarrer_tournoi(self) -> None:
        if self.statut == "En attente":
            self.statut = "En cours"

    def terminer_tournoi(self) -> None:
        if self.statut == "En cours":
            self.statut = "Terminé"

    def sauvegarder_joueurs(self) -> None:
        fichier_joueurs = f"data/tournaments/{self.nom.replace(' ', '_')}_joueurs.json"
        joueurs_data = [joueur.to_dict() for joueur in self.joueurs]
        with open(fichier_joueurs, 'w', encoding='utf-8') as file:
            json.dump(joueurs_data, file, indent=4, ensure_ascii=False)

    