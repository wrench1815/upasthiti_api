# Generated by Django 4.0.6 on 2022-09-01 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_rename_course_name_coursemodel_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='code',
            field=models.CharField(max_length=15),
        ),
    ]