# Generated by Django 4.2.7 on 2024-05-13 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_useraccount_token_alter_useraccount_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_images'),
        ),
    ]
