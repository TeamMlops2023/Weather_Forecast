import unittest 
import requests  
import os       

# Définit une classe de test qui hérite de unittest.TestCase.
class TestFastAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Définit l'URL de base de l'API pour les tests. Utilise la variable d'environnement 'BASE_URL' si elle existe,
        # sinon utilise 'http://localhost:8000' comme valeur par défaut.
        cls.base_url = os.environ.get('BASE_URL', 'http://localhost:8000')

    def test_root_endpoint(self):
        # Teste le endpoint racine ('/').
        print("Testing root endpoint...")
        # Effectue une requête GET au endpoint racine.
        response = requests.get(f"{self.base_url}/")
        # Vérifie que le code de statut de la réponse est 200 (OK).
        self.assertEqual(response.status_code, 200)
        # Vérifie que la réponse JSON correspond à {"Hello": "World"}.
        self.assertEqual(response.json(), {"Hello": "World"})
        print("Root endpoint test passed.")

    def test_status_endpoint(self):
        # Teste le endpoint '/status'.
        print("Testing status endpoint...")
        # Effectue une requête GET au endpoint '/status'.
        response = requests.get(f"{self.base_url}/status")
        # Vérifie que le code de statut de la réponse est 200 (OK).
        self.assertEqual(response.status_code, 200)
        # Vérifie que la réponse JSON correspond à {"status": "ok"}.
        self.assertEqual(response.json(), {"status": "ok"})
        print("Status endpoint test passed.")

    def test_echo_endpoint(self):
        # Teste le endpoint '/echo'.
        print("Testing echo endpoint...")
        test_message = "HelloJenkins"
        # Effectue une requête GET au endpoint '/echo' avec un paramètre 'text'.
        response = requests.get(f"{self.base_url}/echo", params={"text": test_message})
        # Vérifie que le code de statut de la réponse est 200 (OK).
        self.assertEqual(response.status_code, 200)
        # Vérifie que le message testé se trouve dans la réponse.
        self.assertIn(test_message, response.text)
        print("Echo endpoint test passed.")

    # Vous pouvez ajouter ici d'autres méthodes de test pour tester d'autres endpoints de l'API.

# Point d'entrée pour exécuter les tests.
if __name__ == '__main__':
    unittest.main()
