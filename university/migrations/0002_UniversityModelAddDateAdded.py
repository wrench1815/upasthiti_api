# Generated by Django 4.0.6 on 2022-07-12 05:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='universitymodel',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
