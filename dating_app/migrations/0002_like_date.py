# Generated by Django 4.1.5 on 2023-02-11 12:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dating_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
