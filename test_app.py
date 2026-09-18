import unittest
from unittest.mock import patch

from requests.exceptions import ConnectionError

from app import app, log


class Test(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        log.clear()

    def test_get_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.add_animal')
    def test_add_animal(self, mock_add_animal):
        response = self.client.post('/', data={
            "name": "luka",
            "animal": "dog",
            "add_animal": "Add Animals",
        })

        self.assertEqual(response.status_code, 200)
        mock_add_animal.assert_called_once_with("dog", "luka")

    @patch('app.get_animals')
    def test_get_animals(self, mock_get_animals):
        mock_get_animals.return_value = [
            {"name": "Enzo", "animal": "Cat"}
        ]

        response = self.client.post('/', data={
            "get_animals": "Get Animals",
        })

        self.assertEqual(response.status_code, 200)
        mock_get_animals.assert_called_once_with()
        self.assertIn("Enzo", response.get_data(as_text=True))

    @patch('app.requests.get')
    def test_backend_unavailable(self, mock_get):
        mock_get.side_effect = ConnectionError("Backend unavailable")

        response = self.client.post('/', data={
            "get_animals": "Get Animals",
        })

        self.assertEqual(response.status_code, 503)
        self.assertIn(
            "Backend jest chwilowo niedostępny",
            response.get_data(as_text=True),
        )
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
