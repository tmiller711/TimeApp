# Generated by Django 4.1.1 on 2022-09-23 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
