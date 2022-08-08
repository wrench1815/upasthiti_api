# Generated by Django 4.0.6 on 2022-08-08 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('college', '0011_alter_collegemodel_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegemodel',
            name='principal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='administrated_college', to=settings.AUTH_USER_MODEL),
        ),
    ]
