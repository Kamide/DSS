# Generated by Django 2.1.2 on 2018-12-05 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memb_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membapp',
            old_name='is_approved',
            new_name='is_pending',
        ),
    ]
