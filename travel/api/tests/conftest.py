import pytest
import os
from base64 import b64encode
from rest_framework.test import APIClient
from django.core.management import call_command

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
local_test_images_path = 'test_images'


def get_absolute_image_path(image_name):
    relative_path = os.path.join(local_test_images_path, image_name)
    return os.path.join(current_dir_path, relative_path)


def _get_encoded_image_encode(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()

    encoded_image = b64encode(image_data)
    return encoded_image


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db.json')


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def test_post_values():
    encoded_lower_image = _get_encoded_image_encode(get_absolute_image_path("lower.jpg"))
    encoded_upper_image = _get_encoded_image_encode(get_absolute_image_path("upper.jpg"))

    json_values = {
        "beauty_title": "пер. ",
        "title": "Pro",
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

