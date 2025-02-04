# API de Détection du Cancer du Sein

Ce projet fournit une API Flask pour la détection du cancer du sein à l'aide d'un modèle d'apprentissage automatique. Il inclut un système d'authentification JWT et des prédictions interprétables.

## 📋 Table des matières
- [Installation](#installation)
- [Entraînement du modèle](#entraînement-du-modèle)
- [Lancement de l'API](#lancement-de-lapi)
- [Endpoints](#endpoints)
- [Documentation](#documentation)
- [Tests](#tests)
- [Exemple de réponse](#exemple-de-réponse)
- [Structure du projet](#structure-du-projet)

## 📥 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/everi123/breast_cancer_detection.git
cd breast_cancer_detection
```

## Entraînement du Modèle

Pour entraîner le modèle d'apprentissage automatique, exécutez la commande suivante :

```sh
python train_model.py
```

## 🚀 Exécution de l'Application

Pour démarrer le serveur Flask, exécutez :

```sh
python run.py
```

## 🔗 Endpoints

### 🔐 Authentification
- **POST /auth/login** : Authentification utilisateur
- **POST /auth/register** : Inscription d'un nouvel utilisateur

### 🔬 Prédiction
- **POST /predict/predict** : Effectue une prédiction en envoyant les données des caractéristiques

## 📖 Documentation

### POST /auth/login

**Description** : 
Permet à un utilisateur de s'authentifier et d'obtenir un jeton JWT.

**Exemple de requête** :
```json
{
    "email": "testuser@example.com",
    "password": "Test@1234"
}
```

**Exemple de réponse** :
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "email": "testuser@example.com",
    "role": "doctor",
    "username": "testuser"
}
```

### POST /predict/predict

**Description :**
Permet d'envoyer des caractéristiques pour obtenir un diagnostic.

**Exemple de requête :**
```json
{
    "features": {
        "worst area": 515.8,
        "worst concave points": 0.0737,
        "mean concave points": 0.02799,
        "worst radius": 12.88,
        "mean concavity": 0.07741,
        "worst perimeter": 89.61,
        "mean perimeter": 81.47,
        "mean radius": 12.4,
        "mean area": 467.8,
        "worst concavity": 0.2403
    }
}
```

## 🎯 Exemple de réponse

```json
{
    "prediction": "Benign",
    "confidence": 99.0,
    "severity": "Low Risk",
    "message": "Le modèle est très confiant dans un diagnostic bénin. Un suivi régulier est conseillé.",
    "recommended_actions": [
        "Maintenir des contrôles réguliers",
        "Continuer avec la surveillance standard de la santé"
    ],
    "ground_truth": "Benign",
    "correct_prediction": true
}
```

## 📂 Structure du Projet

```bash
breast_cancer_detection/
│── app/
│   │── __init__.py          # Initialisation de l'application Flask
│   │── models/
│   │   ├── user.py          # Définition du modèle utilisateur
│   │── auth/
│   │   ├── routes.py        # Routes pour l'authentification
│   │── predict/
│   │   ├── routes.py        # Routes pour la prédiction
│── config.py                # Configuration de l'application
│── train_model.py           # Script pour entraîner le modèle
│── final_model.pkl          # Modèle entraîné
│── scaler_top.pkl           # Scaler sauvegardé
│── feature_info.json        # Liste des caractéristiques utilisées
│── run.py                   # Point d'entrée de l'application
│── requirements.txt         # Dépendances Python
│── README.md                # Documentation du projet
```