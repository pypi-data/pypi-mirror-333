# Generated by Django 3.1 on 2020-08-27 12:25

import app_kit.generic
import app_kit.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NatureGuidesTaxonNamesView',
            fields=[
                ('name_uuid', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('taxon_author', models.CharField(max_length=100, null=True)),
                ('taxon_nuid', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=5, null=True)),
                ('name_type', models.CharField(choices=[('taxontree', 'TaxonTree'), ('synonym', 'TaxonSynonym'), ('locale', 'TaxonLocale')], max_length=100)),
                ('rank', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MatrixFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(null=True)),
                ('filter_type', models.CharField(choices=[('ColorFilter', 'Color filter'), ('RangeFilter', 'Range filter'), ('NumberFilter', 'Numbers filter'), ('DescriptiveTextAndImagesFilter', 'Descriptive text and images'), ('TaxonFilter', 'Taxonomic filter')], max_length=50)),
                ('definition', models.JSONField(null=True)),
                ('position', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=50)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='MatrixFilterSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoded_space', models.JSONField()),
                ('additional_information', models.JSONField(null=True)),
                ('position', models.IntegerField(default=0)),
                ('matrix_filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.matrixfilter')),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(app_kit.models.ContentImageMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MetaNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxon_latname', models.CharField(max_length=255, null=True)),
                ('taxon_author', models.CharField(max_length=255, null=True)),
                ('taxon_source', models.CharField(max_length=255, null=True)),
                ('taxon_include_descendants', models.BooleanField(default=False)),
                ('taxon_nuid', models.CharField(max_length=255, null=True)),
                ('name_uuid', models.UUIDField(null=True)),
                ('name', models.CharField(max_length=40, null=True)),
                ('node_type', models.CharField(choices=[('root', 'Start'), ('node', 'Node'), ('result', 'Identification result')], max_length=30)),
                ('children_cache', models.JSONField(null=True)),
            ],
            bases=(app_kit.models.UpdateContentImageTaxonMixin, app_kit.models.ContentImageMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NatureGuide',
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
            ],
            options={
                'verbose_name': 'Nature guide',
                'verbose_name_plural': 'Nature guides',
            },
            bases=(app_kit.generic.GenericContentMethodsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NatureGuidesTaxonTree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('taxon_latname', models.CharField(max_length=255)),
                ('taxon_author', models.CharField(max_length=255, null=True)),
                ('taxon_nuid', models.CharField(max_length=255, unique=True)),
                ('rank', models.CharField(max_length=255, null=True)),
                ('is_root_taxon', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=100, null=True, unique=True)),
                ('source_id', models.CharField(max_length=255, unique=True)),
                ('additional_data', models.JSONField(null=True)),
                ('decision_rule', models.CharField(max_length=40, null=True)),
                ('position', models.IntegerField(default=1)),
                ('meta_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.metanode')),
                ('nature_guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.natureguide')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='nature_guides.natureguidestaxontree')),
            ],
            options={
                'ordering': ('position',),
                'unique_together': {('nature_guide', 'taxon_nuid')},
            },
            bases=(app_kit.models.ContentImageMixin, models.Model),
        ),
        migrations.AddField(
            model_name='metanode',
            name='nature_guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.natureguide'),
        ),
        migrations.AddField(
            model_name='matrixfilter',
            name='meta_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.metanode'),
        ),
        migrations.CreateModel(
            name='NodeFilterSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoded_space', models.JSONField(null=True)),
                ('weight', models.IntegerField(default=50)),
                ('matrix_filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.matrixfilter')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.natureguidestaxontree')),
                ('values', models.ManyToManyField(to='nature_guides.MatrixFilterSpace')),
            ],
            options={
                'unique_together': {('node', 'matrix_filter')},
            },
        ),
        migrations.CreateModel(
            name='NatureGuidesTaxonSynonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('taxon_latname', models.CharField(max_length=255)),
                ('taxon_author', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField(max_length=100, null=True, unique=True)),
                ('source_id', models.CharField(max_length=255)),
                ('additional_data', models.JSONField(null=True)),
                ('taxon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.natureguidestaxontree', to_field='name_uuid')),
            ],
            options={
                'unique_together': {('taxon', 'taxon_latname', 'taxon_author')},
            },
        ),
        migrations.CreateModel(
            name='NatureGuidesTaxonLocale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=2)),
                ('iso6392', models.CharField(max_length=3, null=True)),
                ('language_region', models.CharField(max_length=5, null=True)),
                ('preferred', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=100, null=True, unique=True)),
                ('additional_data', models.JSONField(null=True)),
                ('taxon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nature_guides.natureguidestaxontree', to_field='name_uuid')),
            ],
            options={
                'index_together': {('taxon', 'language')},
            },
        ),
        migrations.CreateModel(
            name='NatureGuideCrosslinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision_rule', models.CharField(max_length=40, null=True)),
                ('position', models.IntegerField(default=0)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_node', to='nature_guides.natureguidestaxontree')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_node', to='nature_guides.natureguidestaxontree')),
            ],
            options={
                'ordering': ('position',),
                'unique_together': {('parent', 'child')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='metanode',
            unique_together={('nature_guide', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='matrixfilter',
            unique_together={('meta_node', 'name')},
        ),
    ]
