# Generated by Django 2.1.2 on 2018-12-02 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_cohort'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]
