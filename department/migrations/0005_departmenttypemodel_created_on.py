# Generated by Django 4.0.5 on 2022-06-17 13:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0004_departmenttypemodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmenttypemodel',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]