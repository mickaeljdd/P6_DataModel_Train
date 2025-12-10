from fastapi.testclient import TestClient
from main import app
import sys

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True
    print("Health check passed!")

def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
    print("Swagger UI check passed!")

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Le modèle fonctionne sur FastAPI",
        "docs_url": "/docs"
    }
    print("Vérification du endpoint racine réussie !")

def test_predict(client):
    # Données exemples correspondant au schéma
    # "YearBuilt", "PropertyGFATotal", "HasElectricity", "HasSteam", "HasNaturalGas", "NumberofFloors"
    payload = {
        "YearBuilt": 2000,
        "PropertyGFATotal": 50000,
        "HasElectricity": True,
        "HasSteam": False,
        "HasNaturalGas": True,
        "NumberofFloors": 5
    }
    
    response = client.post("/predict", json=payload)
    
    if response.status_code == 200:
        print(f"Résultat de la prédiction : {response.json()}")
        assert "prediction" in response.json()
        assert isinstance(response.json()["prediction"], float)
    else:
        print(f"La prédiction a échoué avec un statut inattendu {response.status_code} : {response.text}")
        assert False, f"Code de statut inattendu : {response.status_code}"
    
    print("Test de prédiction réussi !")

if __name__ == "__main__":
    try:
        # Utiliser TestClient comme gestionnaire de contexte pour déclencher les événements de durée de vie
        with TestClient(app) as client:
            test_read_root(client)
            test_docs(client)
            test_health(client)
            test_predict(client)
        print("\nTous les tests ont réussi !")
    except AssertionError as e:
        print(f"\nLe test a échoué : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUne erreur s'est produite : {e}")
        sys.exit(1)
