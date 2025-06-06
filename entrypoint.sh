#!/bin/bash

# Démarrer le serveur Ollama en arrière-plan
ollama serve &

# Attendre que le serveur soit prêt
until curl -s http://localhost:11434 > /dev/null; do
  echo "En attente du démarrage de Ollama..."
  sleep 1
done

# Télécharger le modèle
ollama pull llama3.2:3b

# Lancer Streamlit
streamlit run Analyseur_de_Tweet.py --server.address 0.0.0.0