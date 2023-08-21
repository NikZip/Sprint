from django.db import models
from django.db.models import QuerySet


class PerevalAddModel(models.Model):
    STATUS_CHOICES = (
        ('new', 'new'),
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )
    beauty_title = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    other_titles = models.CharField(max_length=50)
    connect = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    time_created = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey('PerevalUser', on_delete=models.SET_DEFAULT, default=None, null=True)
    coords = models.ForeignKey('CoordsModel', on_delete=models.CASCADE)
    level = models.ForeignKey('PerevalLevelsModel', on_delete=models.CASCADE)

    class Meta:
        db_table = 'pereval_added'

    def get_user(self) -> 'PerevalUser':
        return self.created_by

    def get_coords(self) -> 'CoordsModel':
        return self.coords

    def get_level(self) -> 'PerevalLevelsModel':
        return self.level

    def get_images(self) -> 'QuerySet[PerevalImageModel]':
        return self.images.select_related().all().order_by('id')


class CoordsModel(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=4)
    longitude = models.DecimalField(max_digits=9, decimal_places=4)
    height = models.DecimalField(max_digits=9, decimal_places=4)

    class Meta:
        db_table = 'pereval_coords'


class PerevalLevelsModel(models.Model):
    winter = models.CharField(max_length=10, blank=True, null=True)
    summer = models.CharField(max_length=10, blank=True, null=True)
    autumn = models.CharField(max_length=10, blank=True, null=True)
    spring = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'pereval_levels'


class PerevalImageModel(models.Model):
    pereval = models.ForeignKey(PerevalAddModel, on_delete=models.CASCADE, related_name='images')
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField()
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'pereval_images'


class PerevalUser(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)

    class Meta:
        db_table = 'pereval_users'