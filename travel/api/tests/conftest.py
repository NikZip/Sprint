import pytest
from base64 import b64encode
from rest_framework.test import APIClient
from ..utils import PerevalRepositoryDjango


def _get_encoded_image_encode(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()

    encoded_image = b64encode(image_data)
    return encoded_image


@pytest.fixture
def populate_db(test_post_values):
    repository = PerevalRepositoryDjango()
    repository.add_pereval(test_post_values)


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def test_post_values():
    encoded_lower_image = _get_encoded_image_encode("test_images/lower.jpg")
    encoded_upper_image = _get_encoded_image_encode("test_images/upper.jpg")

    json_values = {
        "beauty_title": "пер. ",
        "title": "Прокова",
        "other_titles": "Триев",
        "connect": "",
        "user": {"email": "qwerty@mail.ru",
                 "fam": "Пупкин",
                 "name": "Василий",
                 "otc": "Иванович",
                 "phone": "+7 555 55 55"},
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"},

        "level": {"winter": "",
                  "summer": "1А",
                  "autumn": "1А",
                  "spring": ""},

        "images": [{"data": encoded_upper_image, "title": "Седловина"},
                   {"data": encoded_lower_image, "title": "Подъём"}]
    }
    return json_values

