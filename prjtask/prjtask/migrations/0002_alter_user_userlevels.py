# Generated by Django 3.2.2 on 2021-08-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prjtask', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userlevels',
            field=models.IntegerField(blank=True, choices=[(2, 'worker'), (1, 'manager')], default=2),
        ),
    ]
