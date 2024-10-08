# Generated by Django 4.2.3 on 2023-11-26 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_plantedoutsidelandregistration_geom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agriplot',
            name='AgriplotID',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='District',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Estate',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='GHG_LUC',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='ID_Mill',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Mill_Name',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Ownership',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Planted_Ar',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Province',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='RiskAssess',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Status',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='SubDistric',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Subsidiary',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='TypeOfSupp',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='Village',
        ),
        migrations.RemoveField(
            model_name='agriplot',
            name='YearUpdate',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='Daerah',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='ID_Daerah',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='ID_Mukim',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='ID_Negeri',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='Mukim',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='Negeri',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='Note',
        ),
        migrations.RemoveField(
            model_name='plantedoutsidelandregistration',
            name='Status',
        ),
        migrations.AddField(
            model_name='agriplot',
            name='agriplot_id',
            field=models.CharField(help_text='agriplot_id', max_length=255, null=True, verbose_name='agriplot_id'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='planted_area',
            field=models.CharField(help_text='planted_area', max_length=255, null=True, verbose_name='planted_area'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='risk_assess',
            field=models.CharField(help_text='risk_assess', max_length=255, null=True, verbose_name='risk_assess'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='sub_district',
            field=models.CharField(help_text='sub_district', max_length=255, null=True, verbose_name='sub_district'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='type_of_supplier',
            field=models.CharField(help_text='type_of_supplier', max_length=255, null=True, verbose_name='type_of_supplier'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='year_update',
            field=models.CharField(help_text='year_update', max_length=255, null=True, verbose_name='year_update'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='country',
            field=models.CharField(help_text='country', max_length=255, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='district',
            field=models.CharField(help_text='district', max_length=255, null=True, verbose_name='district'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='estate',
            field=models.CharField(help_text='estate', max_length=255, null=True, verbose_name='estate'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='ghg_luc',
            field=models.CharField(help_text='ghg_luc', max_length=255, null=True, verbose_name='ghg_luc'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='id_mill',
            field=models.CharField(help_text='id_mill', max_length=255, null=True, verbose_name='id_mill'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='mill_name',
            field=models.CharField(help_text='mill_name', max_length=255, null=True, verbose_name='mill_name'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='ownership',
            field=models.CharField(help_text='ownership', max_length=255, null=True, verbose_name='ownership'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='province',
            field=models.CharField(help_text='province', max_length=255, null=True, verbose_name='province'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='status',
            field=models.CharField(help_text='status', max_length=255, null=True, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='subsidiary',
            field=models.CharField(help_text='subsidiary', max_length=255, null=True, verbose_name='subsidiary'),
        ),
        migrations.AddField(
            model_name='agriplot',
            name='village',
            field=models.CharField(help_text='village', max_length=255, null=True, verbose_name='village'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='country',
            field=models.CharField(help_text='country', max_length=255, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='daerah',
            field=models.CharField(help_text='daerah', max_length=255, null=True, verbose_name='daerah'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='id_daerah',
            field=models.CharField(help_text='id_daerah', max_length=255, null=True, verbose_name='id_daerah'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='id_mukim',
            field=models.CharField(help_text='id_mukim', max_length=255, null=True, verbose_name='id_mukim'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='id_negeri',
            field=models.CharField(help_text='id_negeri', max_length=255, null=True, verbose_name='id_negeri'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='mukim',
            field=models.CharField(help_text='mukim', max_length=255, null=True, verbose_name='mukim'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='negeri',
            field=models.CharField(help_text='negeri', max_length=255, null=True, verbose_name='negeri'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='note',
            field=models.CharField(help_text='note', max_length=255, null=True, verbose_name='note'),
        ),
        migrations.AddField(
            model_name='plantedoutsidelandregistration',
            name='status',
            field=models.CharField(help_text='status', max_length=255, null=True, verbose_name='status'),
        ),
    ]
