# Generated by Django 4.0.4 on 2022-06-01 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegemodel',
            name='financial_model',
            field=models.CharField(choices=[('Govt. Funded', 'Govt. Funded'), ('Self Financed', 'Self Financed'), ('Public Private Partnership (PPP)', 'Public Private Partnership (PPP)')], max_length=33),
        ),
        migrations.AlterField(
            model_name='collegemodel',
            name='institute_for',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Co-Education', 'Co-Education')], max_length=14),
        ),
        migrations.AlterField(
            model_name='collegemodel',
            name='location_type',
            field=models.CharField(choices=[('Rural', 'Rural'), ('Urban', 'Urban'), ('Semi-Urban', 'Semi-Urban')], max_length=11),
        ),
    ]
