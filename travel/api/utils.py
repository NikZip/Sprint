from abc import ABC, abstractmethod
from ..models import *


class PerevalRepositoryInterface(ABC):
    @abstractmethod
    def add_pereval(self, pereval_data):
        pass


class PerevalRepositoryDjango(PerevalRepositoryInterface):
    import django

    django.setup()

    @staticmethod
    def _add_coords(coords_data, pereval):
        CoordsModel.objects.create(
            pereval=pereval,
            latitude=coords_data['latitude'],
            longitude=coords_data['longitude'],
            height=coords_data['height'],
        )

    @staticmethod
    def _add_levels(levels_data, pereval):
        PerevalLevelsModel.objects.create(
            pereval=pereval,
            winter=levels_data['winter'],
            summer=levels_data['summer'],
            autumn=levels_data['autumn'],
            spring=levels_data['spring'],
        )

    @staticmethod
    def _add_images(images_data, pereval):
        for image_data in images_data:
            PerevalImageModel.objects.create(
                pereval=pereval,
                image=str.encode(image_data['data']),  # Я не понял почему он преобразуется в str
                desc=image_data['title'],
            )

    @staticmethod
    def _add_user(user_data):
        user = PerevalUser.objects.create(
            email=user_data['email'],
            phone=user_data['phone'],
            fam=user_data['fam'],
            name=user_data['name'],
            otc=user_data['otc'],
        )
        return user

    def add_pereval(self, pereval_data):
        user_data = pereval_data['user']
        creator = self._add_user(user_data)

        pereval = PerevalAddModel.objects.create(
            beauty_title=pereval_data['beauty_title'],
            title=pereval_data['title'],
            other_titles=pereval_data['other_titles'],
            connect=pereval_data['connect'],
            created_by=creator,
        )

        self._add_coords(pereval_data['coords'], pereval)
        self._add_levels(pereval_data['level'], pereval)
        self._add_images(pereval_data['images'], pereval)

        return pereval.pk


