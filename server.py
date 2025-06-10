from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI()

# CORS : autoriser tout (en dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise LLM Ollama
llm = ChatOllama(model="llama3.2")

# Outil de recherche web DuckDuckGo (outil LangChain)
duckduckgo_search = DuckDuckGoSearchRun()

# Prompt personnalisé (contexte)
prompt_context = """
Tu es un assistant intelligent spécialisé dans la détection de fausses informations (fake news).
Ton rôle est d'analyser un post et de déterminer si son contenu est crédible, trompeur ou manifestement faux.

Pour cela, tu peux utiliser l'outil `web_search` qui te permet d'effectuer des recherches sur le Web afin de vérifier les faits, trouver des sources fiables, ou confirmer l'existence d'événements ou de déclarations. Utilise cet outil chaque fois que tu as un doute ou qu'un énoncé semble suspect.

Voici les éléments que tu dois surveiller :
- Langage sensationnaliste ou alarmiste, abus de majuscules ou ponctuation excessive.
- Fautes d'orthographe importantes qui peuvent trahir un manque de professionnalisme.
- Affirmations extraordinaires sans preuves ou sans mention de sources officielles.
- Thèmes conspirationnistes, pseudoscientifiques ou à visée manipulatrice.
- Absence totale de trace dans les médias fiables ou les bases de données publiques.

Structure attendue de ta réponse :
1. Une **analyse critique du contenu**, en expliquant ce qui soulève des doutes ou au contraire ce qui semble plausible.
2. Un résumé de ce que tu as trouvé via la recherche Web (si utilisée).
3. Un **verdict final** clair parmi :  VRAI / FAKE NEWS / NON VÉRIFIABLE

Exemples :

🔹 Exemple 1 :
Post : "Donald Trump va rouvrir la prison d'Alcatraz pour y enfermer les pires criminels démocrates."
→ Analyse : Cette affirmation est sensationnaliste et aucune déclaration officielle ou source fiable n'en parle.
→ Recherche : Aucune trace de cette annonce sur les sites d'actualités sérieux.
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

# Création de l'agent React avec LLM, outil et prompt
web_search_agent = create_react_agent(
    llm,
    tools=[duckduckgo_search],
    prompt=prompt_context
)

# Modèle Pydantic pour requête POST
class PostRequest(BaseModel):
    post_text: str

# Route POST pour analyser un texte
@app.post("/check_fake_news")
async def check_fake_news(req: PostRequest):
    query = f"Est-ce que ce post est une fake news : \"{req.post_text}\" ?"
    result = web_search_agent.invoke({"messages": [HumanMessage(content=query)]})
    return {"analysis": result["messages"][-1].content}
