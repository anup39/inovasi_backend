# Generated by Django 4.2.3 on 2023-11-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_plantedoutsidelandregistration_ttp_source_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='mill',
            name='mill_eq_id',
            field=models.CharField(help_text='mill_eq_id', max_length=255, null=True, verbose_name='mill_eq_id'),
        ),
        migrations.AddField(
            model_name='mill',
            name='mill_name',
            field=models.CharField(help_text='mill_name', max_length=255, null=True, verbose_name='mill_name'),
        ),
        migrations.AddField(
            model_name='mill',
            name='mill_uml_id',
            field=models.CharField(help_text='mill_uml_id', max_length=255, null=True, verbose_name='mill_uml_id'),
        ),
    ]
