# Generated by Django 4.2 on 2023-07-09 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_clade_organism_clade_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='end_coordinate',
        ),
        migrations.RemoveField(
            model_name='domain',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='domain',
            name='start_coordinate',
        ),
        migrations.RemoveField(
            model_name='protein',
            name='organism',
        ),
        migrations.CreateModel(
            name='ProteinDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_coordinate', models.IntegerField()),
                ('end_coordinate', models.IntegerField()),
                ('domain_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.domain')),
                ('protein_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.protein')),
            ],
        ),
        migrations.CreateModel(
            name='OrganismProtein',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.protein')),
                ('taxa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organism')),
            ],
        ),
        migrations.AddIndex(
            model_name='proteindomain',
            index=models.Index(fields=['domain_id', 'protein_id'], name='api_protein_domain__7e197d_idx'),
        ),
        migrations.AddIndex(
            model_name='organismprotein',
            index=models.Index(fields=['taxa_id', 'protein_id'], name='api_organis_taxa_id_f15a32_idx'),
        ),
    ]
