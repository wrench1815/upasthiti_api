# Generated by Django 4.1.1 on 2022-09-27 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0014_collegemodel_teacher'),
        ('student', '0016_alter_collegerollno_class_roll_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='class_roll_no',
            field=models.CharField(default='123', max_length=15, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='college.collegemodel'),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='university_roll_no',
            field=models.CharField(default='123', max_length=15, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
