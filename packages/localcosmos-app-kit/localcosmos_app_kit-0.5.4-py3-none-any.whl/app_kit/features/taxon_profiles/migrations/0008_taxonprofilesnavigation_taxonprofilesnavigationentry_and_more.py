# Generated by Django 4.2 on 2024-08-28 12:00

import app_kit.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxon_profiles', '0007_alter_taxonprofile_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxonProfilesNavigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified_at', models.DateTimeField(null=True)),
                ('prerendered', models.JSONField(null=True)),
                ('last_prerendered_at', models.DateTimeField(null=True)),
                ('taxon_profiles', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='taxon_profiles.taxonprofiles')),
            ],
        ),
        migrations.CreateModel(
            name='TaxonProfilesNavigationEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=355, null=True)),
                ('description', models.TextField(null=True)),
                ('position', models.IntegerField(default=0)),
                ('navigation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxon_profiles.taxonprofilesnavigation')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='taxon_profiles.taxonprofilesnavigationentry')),
            ],
            options={
                'ordering': ('position', 'name'),
            },
            bases=(app_kit.models.ContentImageMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TaxonProfilesNavigationEntryTaxa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxon_latname', models.CharField(max_length=255)),
                ('taxon_author', models.CharField(max_length=255, null=True)),
                ('taxon_source', models.CharField(max_length=255)),
                ('taxon_include_descendants', models.BooleanField(default=False)),
                ('taxon_nuid', models.CharField(max_length=255)),
                ('name_uuid', models.UUIDField()),
                ('navigation_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxon_profiles.taxonprofilesnavigationentry')),
            ],
            options={
                'unique_together': {('navigation_entry', 'name_uuid')},
            },
        ),
    ]
