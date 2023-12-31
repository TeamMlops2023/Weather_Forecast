import unittest
import requests

class TestFastAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://172.17.0.3:8000"  # Remplacez par l'adresse IP du conteneur

    def test_root_endpoint(self):
        """Test du endpoint racine."""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_status_endpoint(self):
        """Test du endpoint /status."""
        response = requests.get(f"{self.base_url}/status")
        self.assertEqual(response.status_code, 200)
        # Adaptez cette vérification au contenu attendu de la réponse
        self.assertEqual(response.json(), {"status": "ok"})

    def test_echo_endpoint(self):
        """Test du endpoint /echo."""
        test_message = "HelloJenkins"
        response = requests.get(f"{self.base_url}/echo", params={"text": test_message})
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_message, response.text)

    # Ajoutez d'autres tests pour les endpoints supplémentaires ici

if __name__ == '__main__':
    unittest.main()
