# Generated by Django 3.1 on 2020-08-27 12:25

import app_kit.generic
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('primary_language', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=255, null=True)),
                ('published_version', models.IntegerField(null=True)),
                ('current_version', models.IntegerField(default=1)),
                ('is_locked', models.BooleanField(default=False)),
                ('messages', models.JSONField(null=True)),
                ('global_options', models.JSONField(null=True)),
                ('map_type', models.CharField(choices=[('observations', 'Observations')], default='observations', max_length=255)),
            ],
            options={
                'verbose_name': 'Map',
                'verbose_name_plural': 'Maps',
            },
            bases=(app_kit.generic.GenericContentMethodsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MapGeometries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry_type', models.CharField(choices=[('project_area', 'Project area')], max_length=255)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=3857)),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.map')),
            ],
        ),
    ]
