# Generated by Django 2.1.2 on 2018-12-04 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MembApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_interests', models.CharField(max_length=100)),
                ('extra_details', models.TextField(null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
