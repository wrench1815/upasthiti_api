# Generated by Django 4.0.5 on 2022-06-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image_public_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]