import os
from google import genai
from google.genai import types
from data_models import ResultatCoach # Import des classes Pydantic
import json
import streamlit as st
# Assurez-vous que la clé API est définie dans votre environnement (GEMINI_API_KEY)
# Si vous utilisez un autre LLM, remplacez cette partie par son SDK (ex: openai.OpenAI())

def creer_prompt_raisonnement(inputs: dict) -> str:
    """Construit un prompt détaillé exigeant le Chain of Thought et l'Auto-Correction."""
    
    # Extraction des inputs pour le prompt
    objectif = inputs.get('objectif')
    sexe = inputs.get('sexe')
    poids = inputs.get('poids')
    taille = inputs.get('taille')
    age = inputs.get('age')
    niveau_activite = inputs.get('niveau_activite')
    contraintes_sante = inputs.get('contraintes_sante')
    disponibilites_sport = inputs.get('disponibilites_sport')
    
    prompt = f"""
    Tu es un **Agent Coach de Santé IA de haute fiabilité**. Ton rôle est de générer un programme complet (Nutrition et Sport) pour un utilisateur, en t'assurant que ce programme soit **sécurisé, personnalisé et atteignable**.

    **Profil Utilisateur :**
    - Objectif : {objectif}
    - Sexe : {sexe}, Âge : {age} ans, Poids : {poids} kg, Taille : {taille} cm
    - Niveau d'activité (hors programme) : {niveau_activite}
    - **Contraintes Médicales/Régimes (TRÈS IMPORTANT) :** {contraintes_sante}
    - Disponibilités Sportives : {disponibilites_sport}

    ---
    **PROTOCOLE DE RAISONNEMENT AVANCÉ (OBLIGATOIRE)**
    Tu dois absolument suivre ces étapes dans ton Log de Raisonnement (`logs_raisonnement`) AVANT de générer le plan final.

    ### Phase 1 : Planification (Chain of Thought - CoT)
    1. **Calcul des Besoins :** Estimez le TDEE (Total Daily Energy Expenditure) approximatif de l'utilisateur. Calculez ensuite l'apport calorique cible nécessaire pour atteindre l'objectif ('{objectif}'). (Ajouter/Retirer 300-500 kcal par exemple).
    2. **Détermination des Macros :** Définissez la répartition idéale en macronutriments (P/L/G) pour cet objectif.
    3. **Intégration des Contraintes :** Analysez la section 'Contraintes Médicales/Régimes'. Déduisez les aliments ou approches nutritionnelles strictement interdites ou obligatoires. Justifiez cette adaptation.
    4. **Plan Sportif :** Élaborez une stratégie d'entraînement (nombre et type de séances) basée sur l'objectif et les disponibilités.

    ### Phase 2 : Validation (Self-Correction/Critique)
    5. **Critique Initiale :** Effectuez une "génération silencieuse" d'un jour type de menu. Critiquez-le immédiatement : Les repas générés respectent-ils les macros cibles ? Le total calorique est-il dans une marge de 50 kcal ? **Y a-t-il une erreur de sécurité (ex: ingrédient interdit par les contraintes) ?**
    6. **Correction Finale :** Si des erreurs sont identifiées à l'étape 5, expliquez la correction effectuée.

    ---
    **INSTRUCTIONS DE SORTIE**
    Générez le programme complet pour **7 jours de nutrition** (ou 4 jours types + 3 jours spécifiques si plus pertinent) et le plan sportif détaillé en utilisant STRICTEMENT la structure JSON fournie par la classe `ResultatCoach`.
    """
    return prompt

def agent_de_sante(inputs: dict) -> ResultatCoach:
    """Initialise l'agent Gemini et exécute le raisonnement pour générer le programme."""
    try:
        # 1. Initialisation du client et du modèle
        client = genai.Client()
        # Modèle de haute performance et structuration pour la fiabilité
        model = 'gemini-2.5-flash' 
        
        # 2. Préparation du prompt et de la structure Pydantic
        system_instruction = "Tu es un Agent Coach de Santé IA de haute fiabilité. Tu dois TOUJOURS répondre en générant un objet JSON qui se conforme STRICTEMENT au schéma Pydantic fourni."
        prompt = creer_prompt_raisonnement(inputs)
        
        # 3. Configuration de la réponse structurée (JSON Schema de Pydantic)
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=ResultatCoach,
        )

        # 4. Appel à l'Agent
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=config,
        )

        # 5. Parsing de la réponse JSON en objet Pydantic
        # Le SDK parse déjà le JSON en une instance de ResultatCoach
        
        # Le contenu de la réponse est une chaîne JSON, nous devons la parser manuellement en Pydantic
        # lorsque l'API retourne la chaîne JSON dans response.text
        
        # Si le modèle est bien configuré pour retourner le JSON, response.text contient le JSON
        data = json.loads(response.text)
        return ResultatCoach.model_validate(data)

    except Exception as e:
        st.error(f"Erreur lors de l'exécution de l'Agent IA : {e}")
        # Dans un vrai cas, on logguerait l'erreur
        return None