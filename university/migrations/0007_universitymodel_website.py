# Generated by Django 4.0.6 on 2022-08-09 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0006_SetDefaultDistrict'),
    ]

    operations = [
        migrations.AddField(
            model_name='universitymodel',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
