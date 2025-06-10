# Utiliser une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Installer Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances Python
RUN pip install --no-cache-dir -e .

# Créer le répertoire pour les modèles
RUN mkdir -p /app/models

# Copier les fichiers de l'application
COPY server.py entrypoint.sh ./

# Rendre le script d'entrée exécutable
RUN chmod +x entrypoint.sh

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Définir la commande de démarrage
CMD ["./entrypoint.sh"] 