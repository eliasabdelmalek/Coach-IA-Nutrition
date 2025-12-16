# Coach-IA-Nutrition

🥗 Projet IA Générative : Coach de Santé avec Nutrition Intelligente
1. Description du Projet
Ce projet consiste à développer un Agent Coach de Santé intelligent utilisant la Generative AI (via l'API Gemini de Google) pour créer des programmes nutritionnels et sportifs entièrement personnalisés.

L'objectif est de dépasser la simple génération de texte en implémentant des techniques de raisonnement avancé qui garantissent la fiabilité et la sécurité des recommandations, notamment en tenant compte des objectifs spécifiques (perte de poids, prise de muscle) et des contraintes utilisateur (allergies, antécédents médicaux).

Le programme complet est généré et présenté via une interface interactive développée avec Streamlit.

Membres de l'Équipe
Wacim Ouzaid
Mohammed Maouni
Idriss Pacotto
Elias Abdelmalek

2. Fonctionnalités Clés
   
Analyse de Profil : Calcul des besoins caloriques et des macronutriments cibles basé sur l'objectif, l'âge, le poids et l'activité.
Programme Nutritionnel : Génération de menus journaliers détaillés avec répartition des macros/calories, adaptés aux contraintes (régimes, allergies).
Programme Sportif : Création d'exercices personnalisés alignés sur le niveau et les contraintes temporelles de l'utilisateur.
Liste de Courses : Production automatique d'une liste de courses cohérente avec les menus proposés.
Visualisation du Raisonnement : Affichage de la chaîne de pensée de l'Agent pour justifier les choix et démontrer la fiabilité du processus (critère essentiel du cours).

3. Choix de la Technique de Raisonnement (Exigence du Cours)
   
Le cœur de ce projet repose sur la mise en œuvre explicite de techniques de raisonnement pour garantir la haute fiabilité du plan généré. Nous avons choisi une architecture hybride combinant le Chain of Thought (CoT) et la Self-Correction (Réflexion), orchestrée par un Agent LLM structuré via Pydantic.

A. Chain of Thought (CoT) pour la Planification

La technique CoT est utilisée pour forcer l'Agent à décomposer la tâche complexe de génération de programme en étapes logiques et traçables.

Analyse Initiale : Calcul du TDEE et détermination de l'apport calorique cible net.
Macro-Distribution : Définition de la répartition P/L/G idéale en fonction de l'objectif (ex: plus de protéines pour la prise de muscle).
Intégration des Contraintes : Vérification de toutes les contraintes (médicales, régimes) et adaptation des choix d'ingrédients.
Stratégie de Génération : Élaboration du plan nutritionnel et sportif en respectant les calculs précédents.

B. Self-Correction (Réflexion) pour la Fiabilité

Après la première phase de planification, l'Agent procède à une phase d'auto-critique avant de finaliser la réponse.
Critique Interne : L'Agent vérifie si le plan initial généré contient des erreurs (ex: dépassement des calories cibles, inclusion d'un aliment interdit par une allergie, erreur de logique sportive).
Génération Corrigée : Si des erreurs sont détectées, l'Agent génère une version finale corrigée.

Cette combinaison garantit que le plan livré à l'utilisateur n'est pas seulement créatif (génération), mais aussi sécurisé et validé (raisonnement). Le Log de Raisonnement est affiché dans l'interface Streamlit pour fournir la preuve de cette boucle de réflexion.

4. Architecture et Installation Technique
   
Prérequis
Python 3.10+

Une clé API Gemini (définie dans la variable d'environnement GEMINI_API_KEY).

Installation

Cloner le dépôt :

git clone VOTRE_URL_DU_DEPOT
cd Coach-IA-Nutrition

Installer les dépendances :

pip install -r requirement.txt

Définir la clé API (MacOS/Linux) :

export GEMINI_API_KEY="VOTRE_CLÉ_API_ICI"

Lancer l'application :

streamlit run app.py

5. Livrables
   
Ce dépôt contient le Code Source nécessaire pour la démo vidéo et l'évaluation. Le fichier README.md fournit l'explication du raisonnement avancé choisi.
