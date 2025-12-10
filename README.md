# API de Prédiction Énergétique des Bâtiments

Ce projet expose une API FastAPI permettant de prédire la consommation énergétique d'un site (`SiteEnergyUseWN`) en fonction des caractéristiques du bâtiment.

## Prérequis

- Python 3.8+
- Un environnement virtuel est recommandé.

## Installation

1. Cloner le repository ou télécharger les fichiers.
2. Créer un environnement virtuel :
   ```bash
   python3 -m venv .venv
   ```
3. Activer l'environnement virtuel :
   - Sur macOS/Linux :
     ```bash
     source .venv/bin/activate
     ```
   - Sur Windows :
     ```bash
     .\.venv\Scripts\Activate
     ```
4. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancer l'API

Vous pouvez lancer l'API de deux manières :

### 1. Avec Uvicorn directement (recommandé pour le développement) :
   ```bash
   uvicorn main:app --reload
   ```

### 2. Via le script Python :
   ```bash
   python main.py
   ```

L'API sera accessible à l'adresse : `http://localhost:8000`

## Documentation de l'API (Swagger UI)

Une fois l'API lancée, vous pouvez accéder à la documentation interactive et tester les endpoints directement via Swagger UI :

- **URL** : [http://localhost:8000/docs](http://localhost:8000/docs)

## Tests

Pour vérifier que tout fonctionne correctement, vous pouvez lancer les tests automatisés :

```bash
python test_api.py
```

Si tout est correct, vous verrez le message : `Tous les tests ont réussi !`

## Structure du Projet

- `main.py` : Le code source de l'API FastAPI.
- `test_api.py` : Script de test pour vérifier la santé, la racine, la documentation et la prédiction.
- `requirements.txt` : Liste des dépendances Python.
- `best_model_cat_gridsearch.joblib` : Le modèle de Machine Learning entraîné (CatBoost).

## Déploiement sur Render.com

Voici les étapes pour déployer cette API gratuitement sur [Render.com](https://render.com) :

1.  **Créer un compte** sur Render.com et connectez votre compte GitHub.
2.  Dans le tableau de bord, cliquez sur **"New +"** et sélectionnez **"Web Service"**.
3.  Connectez le repository GitHub contenant ce projet.
4.  Configurez le service avec les informations suivantes :
    *   **Name** : Le nom de votre service (ex: `building-energy-api`).
    *   **Region** : Choisissez la plus proche de vos utilisateurs (ex: `Frankfurt`).
    *   **Branch** : `main` (ou la branche où se trouve votre code).
    *   **Root Directory** : Laissez vide (ou `.` si demandé).
    *   **Runtime** : `Python 3`.
    *   **Build Command** : `pip install -r requirements.txt`
    *   **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`
5.  Sélectionnez le plan **"Free"**.
6.  Cliquez sur **"Create Web Service"**.

Render va cloner votre code, installer les dépendances et démarrer l'API. Une fois le déploiement terminé, vous aurez une URL (ex: `https://votre-projet.onrender.com`) pour accéder à votre API.

> **Note :** Le premier démarrage peut prendre quelques minutes. N'oubliez pas d'ajouter `/docs` à la fin de l'URL pour accéder à l'interface Swagger (ex: `https://votre-projet.onrender.com/docs`).
