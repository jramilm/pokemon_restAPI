import unittest
import warnings
from main import app


class TestPokemonApi(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<h1>Hello World!</h1>")

    def test_pokemon_page(self):
        response = self.app.get("/api/pokemon")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bulbasaur" in response.data.decode())

    def test_get_by_id(self):
        response = self.app.get("/api/pokemon/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bulbasaur" in response.data.decode())

    def test_filter_name(self):
        response = self.app.get("/api/pokemon/bulbasaur")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bulbasaur" in response.data.decode())

    def test_filter_by_type(self):
        response = self.app.get("/api/pokemon/type/grass")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("grass" in response.data.decode())

    def test_filter_by_ability(self):
        response = self.app.get("/api/pokemon/ability/overgrow")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bulbasaur" in response.data.decode())

    def test_add_pokemon(self):
        data = {"pok_name": 'Drillby', "pok_height": 1, "pok_weight": 23, "pok_base_experience": 34}
        response = self.app.post("/api/pokemon", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Pokemon added successfully", response.get_json()["message"])

    def test_update_pokemon(self):
        data = {"pok_name": 'Gobi', "pok_height": 12, "pok_weight": 12, "pok_base_experience": 100}
        response = self.app.put("/api/pokemon/726", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Pokemon updated successfully", response.get_json()["message"])


if __name__ == '__main__':
    unittest.main()
