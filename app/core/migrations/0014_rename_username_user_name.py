# Generated by Django 4.0.10 on 2023-08-27 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
    ]