# Generated by Django 4.2 on 2023-07-09 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organism',
            old_name='tax_id',
            new_name='taxa_id',
        ),
    ]
