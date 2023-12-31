import requests
import argparse

# Configuration du parser d'arguments pour recevoir l'adresse IP du conteneur
parser = argparse.ArgumentParser(description='Test FastAPI Endpoints.')
parser.add_argument('--container-ip', required=True, help='IP address of the FastAPI container')
args = parser.parse_args()

# Définir l'URL de base de l'API
BASE_URL = f"http://{args.container_ip}:8000"

def test_root_endpoint():
    """ Teste l'endpoint racine. """
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "Hello World" in response.text

def test_status_endpoint():
    """ Teste l'endpoint /status. """
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 200
    assert "ok" in response.text

def test_echo_endpoint():
    """ Teste l'endpoint /echo avec un paramètre. """
    test_message = "HelloJenkins"
    response = requests.get(f"{BASE_URL}/echo", params={"text": test_message})
    assert response.status_code == 200
    assert test_message in response.text

# Ajoutez ici d'autres tests pour d'autres endpoints si nécessaire

if __name__ == "__main__":
    import pytest
    pytest.main()
