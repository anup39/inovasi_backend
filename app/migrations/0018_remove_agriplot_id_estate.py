# Generated by Django 4.2.3 on 2023-11-23 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_mill_mill_eq_id_mill_mill_name_mill_mill_uml_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agriplot',
            name='ID_Estate',
        ),
    ]
