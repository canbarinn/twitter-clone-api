# Generated by Django 4.0.10 on 2023-08-26 21:51

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='./static/media/ayi.png', null=True, upload_to=core.models.user_image_file_path),
        ),
    ]
