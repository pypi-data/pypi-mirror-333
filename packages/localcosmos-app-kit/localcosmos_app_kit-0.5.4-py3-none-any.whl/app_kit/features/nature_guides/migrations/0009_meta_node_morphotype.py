# Generated by Django 4.1.5 on 2023-05-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nature_guides', '0008_meta_node_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='metanode',
            name='morphotype',
            field=models.CharField(max_length=355, null=True),
        ),
    ]
