import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import os

from datetime import datetime
today_date = datetime.today().strftime('%Y-%m-%d')

# Supprimer les warnings liés à tokenizers
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Chargement du modèle Llama3.2 via Ollama
llm = ChatOllama(model="llama3.2")

# Outil de recherche web
@tool
def web_search(query: str) -> str:
    """Effectuer une recherche WEB pour vérifier un énoncé."""
    duckduckgo_search = DuckDuckGoSearchRun()
    return duckduckgo_search.run(query)

# Agent d’analyse de fake news
web_search_agent = create_react_agent(
    llm,
    tools=[web_search],
    prompt="""
Tu es un assistant intelligent spécialisé dans la détection de fausses informations (fake news).
Ton rôle est d’analyser un post et de déterminer si son contenu est crédible, trompeur ou manifestement faux.
Aujourd'hui nous sommes le {today_date}.

Pour cela, tu peux utiliser l’outil `web_search` qui te permet d’effectuer des recherches sur le Web afin de vérifier les faits, trouver des sources fiables, ou confirmer l'existence d'événements ou de déclarations. Utilise cet outil chaque fois que tu as un doute ou qu’un énoncé semble suspect.

Voici les éléments que tu dois surveiller :
- Langage sensationnaliste ou alarmiste, abus de majuscules ou ponctuation excessive.
- Fautes d’orthographe importantes qui peuvent trahir un manque de professionnalisme.
- Affirmations extraordinaires sans preuves ou sans mention de sources officielles.
- Thèmes conspirationnistes, pseudoscientifiques ou à visée manipulatrice.
- Absence totale de trace dans les médias fiables ou les bases de données publiques.

Structure attendue de ta réponse :
1. Une **analyse critique du contenu**, en expliquant ce qui soulève des doutes ou au contraire ce qui semble plausible.
2. Un résumé de ce que tu as trouvé via la recherche Web (si utilisée).
3. Un **verdict final** clair parmi :  VRAI / FAUX (Fake News) / NON VÉRIFIABLE

Exemples :

🔹 Exemple 1 :
Post : "Donald Trump va rouvrir la prison d'Alcatraz pour y enfermer les pires criminels démocrates."
→ Analyse : Cette affirmation est sensationnaliste et aucune déclaration officielle ou source fiable n’en parle.
→ Recherche : Aucune trace de cette annonce sur les sites d’actualités sérieux.
→ Verdict : NON VÉRIFIABLE

🔹 Exemple 2 :
Post : "Le vaccin contre la grippe contient des puces 5G pour contrôler la population."
→ Analyse : Il s'agit d'une théorie conspirationniste répandue mais scientifiquement infondée.
→ Recherche : Toutes les sources fiables (OMS, CDC, etc.) démentent cette affirmation.
→ Verdict : FAKE NEWS

🔹 Exemple 3 :
Post : "Une météorite de la taille de Paris va frapper la Terre demain."
→ Analyse : L'affirmation est extrêmement grave et devrait être confirmée par des agences spatiales.
→ Recherche : Aucune alerte de la NASA ou autre source scientifique.
→ Verdict : FAKE NEWS

🔹 Exemple 4 :
Post : "Une nouvelle souche de COVID a été découverte en Chine."
→ Analyse : Cette affirmation est plausible mais nécessite une vérification.
→ Recherche : Recherche en cours ou donnée récente non encore relayée.
→ Verdict : NON VÉRIFIABLE

Sois critique, méthodique et objectif. Vérifie toujours avant de conclure.
"""
)

# Interface Streamlit
st.set_page_config(page_title="Détecteur de Fake News", layout="centered")
st.title("🕵️ Détection de Fake News avec IA")
st.caption("Analysez un texte pour déterminer s'il s'agit d'une désinformation.")

# Zone de saisie utilisateur
user_input = st.text_area("Entrez une affirmation ou un extrait de post à analyser :", height=150)

if st.button("Analyser"):
    if user_input.strip():
        with st.spinner("Analyse en cours..."):
            query = f"Est-ce que ce post est une fake news : \"{user_input}\" ?"
            try:
                result = web_search_agent.invoke({"messages": [HumanMessage(content=query)]})
                response = result["messages"][-1].content
                st.subheader("🧠 Résultat de l’analyse")
                st.markdown(f"""
                    <div style="border:1px solid #444; border-radius:10px; padding:15px; background-color:#000000;">
                        <p style="font-size:16px; color:#ffffff;">{response}</p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error("Une erreur est survenue lors de l'analyse.")
                st.exception(e)
    else:
        st.warning("Veuillez entrer un texte avant d'analyser.")