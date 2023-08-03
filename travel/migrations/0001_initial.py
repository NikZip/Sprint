# Generated by Django 4.2.3 on 2023-08-03 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PerevalAddModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=50)),
                ('other_titles', models.CharField(max_length=50)),
                ('connect', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('new', 'new'), ('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='new', max_length=10)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_moderated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'pereval_added',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('fam', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('otc', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'pereval_users',
            },
        ),
        migrations.CreateModel(
            name='PerevalLevelsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(max_length=10)),
                ('summer', models.CharField(max_length=10)),
                ('autumn', models.CharField(max_length=10)),
                ('spring', models.CharField(max_length=10)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.perevaladdmodel')),
            ],
            options={
                'db_table': 'pereval_levels',
            },
        ),
        migrations.CreateModel(
            name='PerevalImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image', models.BinaryField()),
                ('desc', models.CharField(max_length=100)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.perevaladdmodel')),
            ],
            options={
                'db_table': 'pereval_images',
            },
        ),
        migrations.CreateModel(
            name='CoordsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=4, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=4, max_digits=9)),
                ('height', models.DecimalField(decimal_places=4, max_digits=9)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.perevaladdmodel')),
            ],
            options={
                'db_table': 'pereval_coords',
            },
        ),
    ]
