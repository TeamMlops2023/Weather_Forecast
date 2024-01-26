from fastapi.testclient import TestClient
from main import app  # Assurez-vous que ce chemin est correct

client = TestClient(app)

def test_get_historical_data_for_sydney():
    # Paramètres pour la requête
    location = "Sydney"
    start_date = "2016-08-01"
    end_date = "2016-08-10"

    # Exécution de la requête à l'API
    response = client.get(
        f"/historical-data?location={location}&start_date={start_date}&end_date={end_date}"
    )

    # Vérification du code de statut et du contenu de la réponse
    assert response.status_code == 200
    data = response.json()
    
    # Assurez-vous que les données retournées correspondent à ce que vous attendez
    assert len(data) > 0  # Il devrait y avoir au moins une entrée
    for record in data:
        assert record['location'] == location
        # Vous pouvez ajouter d'autres assertions ici si nécessaire

# Exécuter le test
if __name__ == "__main__":
    test_get_historical_data_for_sydney()
