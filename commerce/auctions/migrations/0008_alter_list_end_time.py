# Generated by Django 3.2.2 on 2021-06-15 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210614_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]