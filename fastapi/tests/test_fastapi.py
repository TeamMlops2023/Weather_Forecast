# test_fastapi.py
import unittest
import requests

class TestFastAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://172.17.0.3:8000"  # Remplacez par l'IP du conteneur

    def test_root_endpoint(self):
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello World", response.text)

    def test_status_endpoint(self):
        response = requests.get(f"{self.base_url}/status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("ok", response.text)

    # ... autres tests ...

if __name__ == '__main__':
    unittest.main()
