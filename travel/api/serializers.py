from rest_framework import serializers

from ..models import *


class PerevalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalUser
        fields = ['email', 'phone', 'fam', 'name', 'otc']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordsModel
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalLevelsModel
        fields = ['winter', 'summer', 'autumn', 'spring']


class PerevalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImageModel
        fields = ['id', 'image', 'title']


class PerevalAddSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    coords = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = PerevalAddModel
        fields = [
            'id', 'beauty_title', 'title', 'other_titles', 'connect', 'status',
            'time_created', 'time_moderated', 'user', 'coords', 'level', 'images',
        ]

    def get_user(self, obj):
        user = obj.get_user()
        return PerevalUserSerializer(user).data

    def get_coords(self, obj):
        coords = obj.get_coords()
        return CoordsSerializer(coords).data

    def get_level(self, obj):
        level = obj.get_level()
        return LevelSerializer(level).data

    def get_images(self, obj):
        images = obj.get_images()
        return PerevalImagesSerializer(images, many=True).data

