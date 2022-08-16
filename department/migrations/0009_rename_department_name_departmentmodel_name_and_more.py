# Generated by Django 4.0.6 on 2022-08-12 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0008_departmentmodel_college_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='departmentmodel',
            old_name='department_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='departmentmodel',
            name='hod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hod_department', to=settings.AUTH_USER_MODEL),
        ),
    ]