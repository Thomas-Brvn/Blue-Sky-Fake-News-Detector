# Blue Sky Fake News Detector 🔍

## Description
Ce projet est une application web qui permet d'analyser automatiquement les posts publiés sur Bluesky pour détecter les potentielles fake news. L'application utilise l'intelligence artificielle (LLaMA 3.2) et des recherches web en temps réel pour évaluer la crédibilité des informations.

## Fonctionnalités
- 🔎 Recherche et affichage du dernier post public d'un utilisateur Bluesky
- 🤖 Analyse automatique du contenu par un modèle d'IA
- 🌐 Vérification des faits via des recherches web en temps réel
- 📊 Classification des posts en trois catégories : VRAI, FAUX, ou NON VÉRIFIABLE

## Technologies utilisées
- Python
- Streamlit (interface utilisateur)
- LangChain (framework d'IA)
- LLaMA 3.2 (modèle de langage)
- DuckDuckGo (recherche web)
- Bluesky API (via atproto)
- Docker (containerisation)

## Installation

### Option 1 : Installation avec Docker (Recommandée)
1. Assurez-vous d'avoir Docker et Docker Compose installés sur votre machine
2. Clonez le repository :
```bash
git clone [URL_DU_REPO]
cd Blue-Sky-Fake-News-Detector
```
3. Lancez l'application avec Docker Compose :
```bash
docker-compose up --build
```
4. Accédez à l'application dans votre navigateur à l'adresse : `http://localhost:8501`

### Option 2 : Installation manuelle
1. Clonez le repository :
```bash
git clone [URL_DU_REPO]
cd Blue-Sky-Fake-News-Detector
```

2. Installez les dépendances :
```bash
uv venv
source .venv/bin/activate
uv sync
```

3. Installez Ollama et téléchargez le modèle LLaMA 3.2 :
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

4. Configurez les variables d'environnement :
Créez un fichier `.env` avec vos identifiants Bluesky :
```
BLSKY_IDENTIFIER=votre_identifiant
BLSKY_PASSWORD=votre_mot_de_passe
```

## Utilisation
1. Lancez l'application :
```bash
streamlit run Analyseur_de_Tweet.py
```

2. Entrez le nom d'utilisateur Bluesky à analyser (format : username.bsky.social)
3. L'application affichera le dernier post de l'utilisateur et son analyse

## Critères d'analyse
L'IA analyse les posts selon plusieurs critères :
- Langage sensationnaliste ou alarmiste
- Fautes d'orthographe importantes
- Affirmations sans preuves ou sources
- Thèmes conspirationnistes
- Vérification via des sources fiables

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une pull request pour améliorer le code
- Suggérer de nouvelles fonctionnalités

## Licence
[À définir]

## Auteurs
[Votre nom] 