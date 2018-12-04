# Generated by Django 2.1.2 on 2018-12-02 23:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0008_auto_20181201_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='last_edited_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Last_Editor', to=settings.AUTH_USER_MODEL),
        ),
    ]
