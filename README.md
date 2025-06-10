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