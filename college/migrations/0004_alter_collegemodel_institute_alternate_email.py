# Generated by Django 4.0.4 on 2022-06-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0003_rename_running_frm_own_campus_collegemodel_running_from_own_campus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegemodel',
            name='institute_alternate_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='alternate email address'),
        ),
    ]