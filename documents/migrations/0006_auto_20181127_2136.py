# Generated by Django 2.1.2 on 2018-11-28 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20181127_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='locked_by',
            field=models.TextField(),
        ),
    ]
