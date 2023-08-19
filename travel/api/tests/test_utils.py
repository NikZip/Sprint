import django.core.exceptions
import pytest

from ..utils import PerevalRepositoryDjango


class TestDjangoRepository:
    repository = PerevalRepositoryDjango()

    @pytest.mark.django_db
    def test_usual_creation(self, test_post_values):
        result = self.repository.add_pereval(test_post_values)
        assert result.beauty_title == test_post_values['beauty_title']
        assert result.created_by.email == test_post_values['user']['email']
        assert result.coords.latitude == test_post_values['coords']['latitude']
        assert result.level.summer == test_post_values['level']['summer']
        assert result.images.count() == len(test_post_values['images'])

    @pytest.mark.django_db
    def test_creation_if_same_user(self, test_post_values):
        result_1 = self.repository.add_pereval(test_post_values)
        result_2 = self.repository.add_pereval(test_post_values)
        assert result_1.created_by == result_2.created_by

    @pytest.mark.django_db
    def test_creation_if_missing_params(self, test_post_values):
        values_without_secondary_info = {
            "beauty_title": "пер. ",
            "title": "Прокова",
            "other_titles": "Триев",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
        }
        with pytest.raises(KeyError):
            self.repository.add_pereval(values_without_secondary_info)

    @pytest.mark.django_db
    def test_creation_if_wrong_type(self, test_post_values_wrong_types):
        with pytest.raises(django.core.exceptions.ValidationError):
            self.repository.add_pereval(test_post_values_wrong_types)


