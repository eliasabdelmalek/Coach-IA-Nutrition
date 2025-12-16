from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- Pydantic : Structuration des sorties du LLM ---

# 1. Raisonnement (Crucial pour le cours)
class LogEtape(BaseModel):
    """Étape de la chaîne de pensée de l'agent (CoT/Self-Correction)."""
    titre: str = Field(..., description="Titre de l'étape de raisonnement (ex: Calcul des Kcal, Auto-Critique).")
    details: str = Field(..., description="Détails du calcul, de la décision ou de la critique effectuée.")

# 2. Nutrition
class Repas(BaseModel):
    """Détail d'un repas dans le menu journalier."""
    nom: str = Field(..., description="Nom du repas (Petit-déjeuner, Déjeuner, Dîner, Collation).")
    description_plat: str = Field(..., description="Description détaillée du plat (ingrédients et préparation sommaire).")
    calories: int = Field(..., description="Calories estimées pour ce repas.")
    proteines_g: float
    lipides_g: float
    glucides_g: float

class JourNutritionnel(BaseModel):
    """Programme nutritionnel complet pour une journée."""
    jour: str = Field(..., description="Nom du jour ou 'Jour Type'.")
    repas: List[Repas]
    total_kcal_jour: int
    justification_adaptation: str = Field(..., description="Justification que le plan respecte l'objectif et les contraintes (ex: 'Ce jour est riche en protéines et sans gluten').")

# 3. Sport
class ProgrammeSportif(BaseModel):
    """Détail d'une séance d'exercice."""
    jour_semaine: str
    duree_minutes: int
    type_seance: str = Field(..., description="Ex: Force, Cardio, Flexibilité, HIIT.")
    exercices: List[str] = Field(..., description="Liste détaillée des exercices avec séries/répétitions/temps de repos.")

# 4. Résultat Global
class ResultatCoach(BaseModel):
    """La structure globale de la réponse finale de l'agent."""
    logs_raisonnement: List[LogEtape] = Field(..., description="La chaîne de pensée complète (CoT et Self-Correction).")
    
    estimation_kcal_cible: int = Field(..., description="Estimation calorique journalière recommandée par l'agent.")
    macros_cible: str = Field(..., description="Répartition macro-nutrimentaire cible calculée (ex: 40P/30L/30G).")

    plan_nutritionnel: List[JourNutritionnel]
    plan_sportif: List[ProgrammeSportif]
    liste_courses_semaine: List[str] = Field(..., description="Liste de courses complète et regroupée par type d'aliments pour tous les menus générés.")