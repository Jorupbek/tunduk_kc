# Generated by Django 4.2.5 on 2023-12-26 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Дать права на запрос к тундук'),
        ),
    ]
