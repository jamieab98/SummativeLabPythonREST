import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    def test_add_item_success(self):
        payload = {"barcode": "0087692008224", "quantity": 5}
        response = self.client.post("/inventory", json = payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("product_name", data)
        self.assertIn("quantity", data)
        self.assertIn(data["quantity"], 5)

if __name__ == "__main__":
    unittest.main()