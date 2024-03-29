# Generated by Django 4.1.1 on 2022-09-25 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_remove_studentmodel_college_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='college',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='university',
        ),
        migrations.AddField(
            model_name='collegerollno',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_college', to='student.studentmodel'),
        ),
        migrations.AddField(
            model_name='universityrollno',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_university', to='student.studentmodel'),
        ),
    ]
