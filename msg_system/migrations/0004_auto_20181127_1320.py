# Generated by Django 2.1.2 on 2018-11-27 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msg_system', '0003_auto_20181125_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver_archive',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_archive',
            field=models.BooleanField(default='True'),
        ),
    ]
