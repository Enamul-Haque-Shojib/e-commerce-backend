# Generated by Django 4.2.7 on 2024-05-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0004_alter_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothwishlist',
            name='image',
            field=models.URLField(),
        ),
    ]