# Generated by Django 4.0.4 on 2022-06-01 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0002_alter_collegemodel_financial_model_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collegemodel',
            old_name='running_frm_own_campus',
            new_name='running_from_own_campus',
        ),
    ]
