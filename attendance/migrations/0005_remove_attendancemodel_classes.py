# Generated by Django 4.1.1 on 2022-09-23 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_attendancemodel_classes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancemodel',
            name='classes',
        ),
    ]
