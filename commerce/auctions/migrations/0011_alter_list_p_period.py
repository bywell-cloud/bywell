# Generated by Django 3.2.2 on 2021-06-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_list_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='p_period',
            field=models.IntegerField(choices=[(1, '1 Day'), (3, '3 Days'), (7, '1 Week')], default=1),
        ),
    ]
