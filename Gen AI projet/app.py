import streamlit as st
from agent import agent_de_sante # Import de notre agent
from data_models import ResultatCoach # Pour l'affichage typé

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Coach IA de Santé et Nutrition",
    layout="wide"
)

def display_results(resultat: ResultatCoach):
    """Affiche les résultats structurés de l'Agent."""
    
    st.header("✨ Programme Personnalisé Généré")
    
    # --- 1. AFFICHAGE DU RAISONNEMENT (Le point clé du projet) ---
    st.subheader("🧠 Logique et Raisonnement de l'Agent (CoT & Self-Correction)")
    st.info("Ce sont les étapes de pensée et de validation que l'Agent a suivies pour garantir la fiabilité du plan.")
    
    for i, log in enumerate(resultat.logs_raisonnement):
        with st.expander(f"**Étape {i+1}: {log.titre}**"):
            st.markdown(log.details)
            
    st.markdown("---")

    # --- 2. RÉSUMÉ ET PLAN NUTRITIONNEL ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🍽️ Objectifs Calculés")
        st.metric("Calories Cible Journalière", f"{resultat.estimation_kcal_cible} kcal")
    with col_b:
        st.subheader("🔬 Répartition des Macros")
        st.markdown(f"**{resultat.macros_cible}** (Protéines/Lipides/Glucides)")
    
    st.subheader("Menus Journaliers")
    tab_titles = [jour.jour for jour in resultat.plan_nutritionnel]
    tabs = st.tabs(tab_titles)
    
    for i, jour in enumerate(resultat.plan_nutritionnel):
        with tabs[i]:
            st.markdown(f"**Justification :** {jour.justification_adaptation}")
            st.metric("Total Kcal", f"{jour.total_kcal_jour} kcal")
            for repas in jour.repas:
                st.markdown(f"**{repas.nom}** ({repas.calories} kcal)")
                st.markdown(f"*{repas.description_plat}*")
                st.caption(f"Macros: P:{repas.proteines_g}g | L:{repas.lipides_g}g | G:{repas.glucides_g}g")
    
    st.markdown("---")

    # --- 3. PLAN SPORTIF ET LISTE DE COURSES ---
    st.subheader("💪 Programme Sportif")
    for seance in resultat.plan_sportif:
        st.markdown(f"**{seance.jour_semaine}** - **{seance.type_seance}** ({seance.duree_minutes} min)")
        st.markdown("*Exercices :*")
        st.markdown("- " + "\n- ".join(seance.exercices))
    
    st.markdown("---")
    
    st.subheader("🛒 Liste de Courses")
    st.markdown("Voici la liste complète des ingrédients pour la semaine (regroupée par l'Agent) :")
    st.markdown("- " + "\n- ".join(resultat.liste_courses_semaine))


def main():
    st.title("🤖 Coach IA : Programme Nutritionnel & Sportif Personnalisé")
    
    # Création du formulaire (inchangé par rapport à la première étape)
    with st.form("user_input_form"):
        st.header("🎯 Vos Objectifs et Profil")
        col1, col2 = st.columns(2)
        
        with col1:
            objectif = st.selectbox("Objectif principal", ["Perte de poids", "Prise de masse musculaire", "Recomposition corporelle", "Maintien"])
            sexe = st.selectbox("Sexe", ["Homme", "Femme"])
            age = st.number_input("Âge (années)", min_value=18, value=30)
            poids = st.number_input("Poids (kg)", min_value=30.0, value=75.0, step=0.5)
            taille = st.number_input("Taille (cm)", min_value=120, value=175)

        with col2:
            niveau_activite = st.selectbox("Niveau d'activité physique", ["Sédentaire", "Léger", "Modéré", "Intense"])
            st.subheader("⚠️ Contraintes / Antécédents")
            contraintes_sante = st.text_area("Allergies, régimes, antécédents médicaux (ex: Diabète, Végétarien).", placeholder="Ex: Allergie aux noix, végétarien.")
            disponibilites_sport = st.text_area("Disponibilités et préférences sportives (équipement, jours, type).", placeholder="Ex: 3 séances par semaine, préfère la musculation.")

        submitted = st.form_submit_button("Générer mon Programme")

    if submitted:
        # Collecte des données du formulaire dans un dictionnaire
        user_inputs = {
            'objectif': objectif, 'sexe': sexe, 'age': age, 'poids': poids, 'taille': taille,
            'niveau_activite': niveau_activite, 'contraintes_sante': contraintes_sante, 
            'disponibilites_sport': disponibilites_sport
        }
        
        with st.spinner("L'Agent Coach procède à la planification et à l'auto-critique..."):
            programme_genere = agent_de_sante(user_inputs)
        
        if programme_genere:
            display_results(programme_genere)
        else:
            st.error("Impossible de générer le programme. Vérifiez l'état de l'API.")


if __name__ == "__main__":
    main()