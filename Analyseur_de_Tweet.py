import streamlit as st
from atproto import Client
import datetime
import traceback
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

llm = ChatOllama(model="llama3.2")
 
@tool
def web_search(query: str) -> str:
    """Effectuer une recherche WEB.
    
    Args:
        query: The query to search for.
    """
    duckduckgo_search = DuckDuckGoSearchRun()
    return duckduckgo_search.run(query)

web_search_agent = create_react_agent(
    llm,
    tools=[web_search],
    prompt="""
Tu es un assistant intelligent spécialisé dans la détection de fausses informations (fake news).
Ton rôle est d’analyser un post et de déterminer si son contenu est crédible, trompeur ou manifestement faux.

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
3. Un **verdict final** clair parmi :  VRAI / FAUX / NON VÉRIFIABLE

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
→ Verdict : FAUX

🔹 Exemple 3 :
Post : "Une météorite de la taille de Paris va frapper la Terre demain."
→ Analyse : L'affirmation est extrêmement grave et devrait être confirmée par des agences spatiales.
→ Recherche : Aucune alerte de la NASA ou autre source scientifique.
→ Verdict : FAUX

🔹 Exemple 4 :
Post : "Une nouvelle souche de COVID a été découverte en Chine."
→ Analyse : Cette affirmation est plausible mais nécessite une vérification.
→ Recherche : Recherche en cours ou donnée récente non encore relayée.
→ Verdict : NON VÉRIFIABLE

Sois critique, méthodique et objectif. Vérifie toujours avant de conclure.
"""
)

st.set_page_config(page_title="Bluesky Post Viewer", layout="centered")
st.title("🔎 Dernier post public Bluesky d’un utilisateur")
 
# À sécuriser dans secrets ou .env
BLSKY_IDENTIFIER = "trou2balle.bsky.social"
BLSKY_PASSWORD = "qebguk-vudhy5-gAxzer"
 
username = st.text_input("Nom d'utilisateur Bluesky (ex : thomas.bsky.social)")
 
if username:
    try:
        client = Client()
        client.login(BLSKY_IDENTIFIER, BLSKY_PASSWORD)
 
        profile = client.app.bsky.actor.get_profile({'actor': username})
        feed = client.app.bsky.feed.get_author_feed({'actor': username, 'limit': 1})
 
        if feed.feed:
            post = feed.feed[0].post
            post_text = post.record.text
 
            # ✅ Conversion en datetime
            try:
                post_time_str = post.record.created_at
                post_time = datetime.datetime.fromisoformat(post_time_str.replace("Z", "+00:00"))
                post_time_fmt = post_time.strftime('%d %B %Y, %H:%M')
            except Exception:
                post_time_fmt = "Date inconnue"
 
            st.markdown(f"""
                <div style="border:1px solid #ccc; border-radius:10px; padding:10px;">
                    <div style="display:flex; align-items:center;">
                        <img src="{profile.avatar}" style="border-radius:50%; width:48px; height:48px; margin-right:10px;">
                        <div>
                            <strong>{profile.display_name}</strong> <br>
                            <span style="color:gray">@{profile.handle} · {post_time_fmt}</span>
                        </div>
                    </div>
                    <p style="margin-top:10px; font-size:16px;">{post_text}</p>
                </div>
            """, unsafe_allow_html=True)
            query = f"Est-ce que ce post est une fake news : \"{post_text}\" ?"
            web_search_result = web_search_agent.invoke({"messages": [HumanMessage(content=query)]})

            # Afficher la réponse du modèle
            st.subheader("🧠 Analyse par l'assistant IA")
            st.markdown(f"""
            <div style="border:1px solid #333; border-radius:10px; padding:10px; background-color:#000000;">
                <p style="font-size:16px; color:#ffffff;">{web_search_result["messages"][-1].content}</p>
            </div>
        """, unsafe_allow_html=True)
        else:
            st.warning("Aucun post trouvé.")
 
    except Exception as e:
        st.error("Une erreur est survenue.")
        st.text(traceback.format_exc())
