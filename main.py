from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import os

# Définir le modèle de données d'entrée
class BuildingFeatures(BaseModel):
    YearBuilt: int
    PropertyGFATotal: int
    HasElectricity: bool
    HasSteam: bool
    HasNaturalGas: bool
    NumberofFloors: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print(f"Modèle chargé avec succès depuis {MODEL_PATH}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle : {e}")
            model = None
    else:
        print(f"Fichier du modèle introuvable à {MODEL_PATH}")
    yield
    # Logique d'arrêt si nécessaire

# Charger le modèle
MODEL_PATH = "best_model_cat_gridsearch.joblib"
model = None

app = FastAPI(
    title="API de Prédiction Énergétique des Bâtiments",
    description="API pour prédire la consommation énergétique du site en fonction des caractéristiques du bâtiment",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "message": "Le modèle fonctionne sur FastAPI",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(features: BuildingFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    try:
        # Convertir les caractéristiques d'entrée en DataFrame
        # Le modèle attend des noms de colonnes et un ordre spécifiques
        input_data = pd.DataFrame([features.dict()])
        
        # S'assurer que l'ordre des colonnes correspond aux données d'entraînement (de l'analyse du notebook)
        # Colonnes attendues : ["YearBuilt", "PropertyGFATotal", "HasElectricity", "HasSteam", "HasNaturalGas", "NumberofFloors"]
        # Note : SiteEnergyUseWN(kBtu) était la cible, donc elle n'est pas en entrée.
        
        # Faire la prédiction
        prediction = model.predict(input_data)
        
        # la prédiction est un tableau numpy
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
