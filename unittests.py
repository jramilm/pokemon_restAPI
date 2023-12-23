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


if __name__ == '__main__':
    unittest.main()
