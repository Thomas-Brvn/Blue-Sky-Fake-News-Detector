#!/bin/bash

ollama serve &

# Attendre que le serveur soit prêt
until curl -s http://localhost:11434 > /dev/null; do
  echo "En attente du démarrage de Ollama..."
  sleep 1
done

# Télécharger le modèle
ollama pull llama3.2:latest

# Lancer le serveur FastAPI avec uvicorn
uvicorn server:app --host 0.0.0.0 --port 8000