# Fake News Detector

Ce projet est une application de détection de fake news utilisant Docker pour le déploiement.

## Prérequis

- Docker installé sur votre machine
- Git (pour cloner le repository)

## Installation et Lancement

1. Clonez le repository :
```bash
git clone [https://github.com/Thomas-Brvn/Social-Network-Fake-News-Detection.git]
cd [Social-Network-Fake-News-Detection]
```

2. Construisez l'image Docker :
```bash
docker build -t fake-news-detector .
```

3. Lancez le conteneur :
```bash
docker run -p 8000:8000 fake-news-detector
```

Le serveur sera accessible à l'adresse : `http://localhost:8000`

## Arrêt du serveur

Pour arrêter le serveur, utilisez la combinaison de touches `Ctrl + C` dans le terminal où le conteneur est en cours d'exécution.

Pour supprimer le conteneur après utilisation :
```bash
docker rm $(docker ps -a -q)
```

## Notes

- Le port 8000 est exposé pour accéder à l'application
- Assurez-vous qu'aucune autre application n'utilise déjà le port 8000 sur votre machine

----------------------------------------------------------------------------------------------


# 🚀 Product Backlog

Bienvenue sur le backlog du projet de détection de fausses nouvelles. Ce document suit les tâches à accomplir pour mener le projet à bien. Cochez les cases au fur et à mesure de votre avancement !


## ✨ Fonctionnalités (Features)
*Ce sont les nouvelles capacités à construire pour l'utilisateur.*

### Priorité Élevée
- [ ] **Mettre en place le serveur API principal (Back-end)**
  - *Description : Créer la structure de base du serveur avec un framework comme FastAPI, incluant un premier endpoint de test.*
- [ ] **Intégrer le modèle de langage (LLM) pour l'analyse**
  - *Description : Connecter le serveur à un modèle pré-entraîné (via Ollama) pour analyser le contenu textuel d'une URL.*
- [ ] **Développer l'interface utilisateur (Front-end) de base**
  - *Description : Créer une page web simple avec un champ pour entrer une URL et un bouton pour lancer l'analyse.*
- [ ] **Développer/Améliorer l'extension navigateur Bluesky**
  - *Description : Améliorer ou créer l'extension Bluesky permettant de lancer une analyse directement depuis la page visitée.*
- [ ] **Connecter la base de données MongoDB**
  - *Description : Mettre en place la connexion à la base de données pour sauvegarder les résultats des analyses.*

### Priorité Moyenne
- [ ] **Mettre en place un système d'authentification des utilisateurs**
  - *Description : Permettre aux utilisateurs de s'inscrire et de se connecter à l'application.*
- [ ] **Créer une page de profil utilisateur avec historique**
  - *Description : Afficher l'historique des analyses effectuées par l'utilisateur connecté.*
- [ ] **Intégrer l'outil de recherche DuckDuckGo**
  - *Description : Ajouter DuckDuckGo pour obtenir des résultats pertinents lors des recherches.*
- [ ] **Empaqueter et déployer l'extension**
  - *Description : Préparer l'extension pour sa distribution et automatiser son déploiement.*

## 📈 Améliorations (Improvements)
*Ce sont des optimisations des fonctionnalités existantes.*

- [ ] **Améliorer la précision du modèle de détection (Priorité : Élevée)**
  - *Description : Appliquer des techniques de fine-tuning sur le modèle de base avec des données spécifiques aux fausses nouvelles pour améliorer la pertinence des résultats.*
- [ ] **Optimiser les performances de l'API (Priorité : Moyenne)**
  - *Description : Réduire le temps de réponse du serveur en mettant en place un système de cache pour les URLs déjà analysées.*
- [ ] **Enrichir l'affichage des résultats (Priorité : Moyenne)**
  - *Description : Au lieu d'un simple score, afficher des explications sur les raisons de la classification (ex: source non fiable, affirmations contredites, etc.).*

## 🐞 Bogues (Bugs)
*Ce sont des corrections de problèmes dans le code existant.*

- [ ] **Gérer les erreurs d'URL (Priorité : Élevée)**
  - *Description : L'application doit retourner une erreur claire et ne pas planter si l'utilisateur soumet une URL invalide, un lien mort ou une page protégée.*
- [ ] **Sécuriser les endpoints de l'API (Priorité : Élevée)**
  - *Description : Revoir le code de l'API pour prévenir les vulnérabilités de base (ex: injections, accès non autorisé).*

## 🛠️ Dette Technique (Technical Debt)
*Ce sont des tâches internes pour améliorer la qualité et la maintenabilité du code.*

- [ ] **Rédiger les tests unitaires et d'intégration (Priorité : Élevée)**
  - *Description : Écrire des tests automatisés pour les fonctions critiques du back-end afin d'éviter les régressions futures.*
- [ ] **Mettre en place une documentation d'API (Priorité : Moyenne)**
  - *Description : Utiliser un outil comme Swagger (OpenAPI) pour générer une documentation interactive de l'API.*
- [ ] **Améliorer la configuration Docker (Priorité : Moyenne)**
  - *Description : Optimiser le `Dockerfile` et utiliser `docker-compose` pour faciliter le lancement de l'environnement de développement complet.*
