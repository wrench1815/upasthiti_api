# Generated by Django 4.0.5 on 2022-06-18 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0005_remove_collegemodel_affiliating_university_and_more'),
        ('department', '0007_rename_courses_departmentmodel_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentmodel',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='college.collegemodel'),
        ),
        migrations.AlterField(
            model_name='departmentmodel',
            name='department_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='department.departmenttypemodel'),
        ),
    ]
