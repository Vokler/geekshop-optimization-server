# Generated by Django 3.2.11 on 2022-01-22 20:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20220122_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverification',
            old_name='expired',
            new_name='expiration',
        ),
    ]
