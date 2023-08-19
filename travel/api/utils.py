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
    def _add_coords(coords_data) -> CoordsModel:
        coords = CoordsModel.objects.create(
            latitude=coords_data['latitude'],
            longitude=coords_data['longitude'],
            height=coords_data['height'],
        )
        return coords

    @staticmethod
    def _add_levels(levels_data) -> PerevalLevelsModel:
        levels = PerevalLevelsModel.objects.create(
            winter=levels_data['winter'],
            summer=levels_data['summer'],
            autumn=levels_data['autumn'],
            spring=levels_data['spring'],
        )
        return levels

    @staticmethod
    def _add_images(images_data, pereval) -> None:
        for image_data in images_data:
            if type(image_data['data']) is bytes:  # Converting from str bcz of there is no binary field in serializers
                data = image_data['data']
            else:
                data = str.encode(image_data['data'])

            PerevalImageModel.objects.create(
                pereval=pereval,
                image=data,
                title=image_data['title'],
            )

    @staticmethod
    def _add_user(user_data) -> PerevalUser:
        user = PerevalUser.objects.create(
            email=user_data['email'],
            phone=user_data['phone'],
            fam=user_data['fam'],
            name=user_data['name'],
            otc=user_data['otc'],
        )
        return user

    def add_pereval(self, pereval_data) -> PerevalUser.pk:
        try:
            creator = PerevalUser.objects.get(email=pereval_data['user']['email'])
        except PerevalUser.DoesNotExist:
            creator = self._add_user(pereval_data['user'])

        coords = self._add_coords(pereval_data['coords'])
        level = self._add_levels(pereval_data['level'])

        pereval = PerevalAddModel.objects.create(
            beauty_title=pereval_data['beauty_title'],
            title=pereval_data['title'],
            other_titles=pereval_data['other_titles'],
            connect=pereval_data['connect'],
            created_by=creator,
            coords=coords,
            level=level,
        )
        self._add_images(pereval_data['images'], pereval)

        return pereval



