from django.db import models


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
    connect = models.CharField(max_length=100)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    time_created = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey('PerevalUser', on_delete=models.SET_DEFAULT, default=None, null=True)

    class Meta:
        db_table = 'pereval_added'


class CoordsModel(models.Model):
    pereval = models.ForeignKey(PerevalAddModel, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=4)
    longitude = models.DecimalField(max_digits=9, decimal_places=4)
    height = models.DecimalField(max_digits=9, decimal_places=4)

    class Meta:
        db_table = 'pereval_coords'


class PerevalLevelsModel(models.Model):
    pereval = models.ForeignKey(PerevalAddModel, on_delete=models.CASCADE)
    winter = models.CharField(max_length=10)
    summer = models.CharField(max_length=10)
    autumn = models.CharField(max_length=10)
    spring = models.CharField(max_length=10)

    class Meta:
        db_table = 'pereval_levels'


class PerevalImageModel(models.Model):
    pereval = models.ForeignKey(PerevalAddModel, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField()
    desc = models.CharField(max_length=100)

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