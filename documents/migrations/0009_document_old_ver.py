# Generated by Django 2.1.2 on 2018-12-02 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20181201_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='old_ver',
            field=models.TextField(default=''),
        ),
    ]