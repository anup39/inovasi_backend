# Generated by Django 4.2.3 on 2023-12-15 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_remove_agriplot_mill_eq_id_agriplot_millideq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agriplot',
            name='millideq',
        ),
    ]
