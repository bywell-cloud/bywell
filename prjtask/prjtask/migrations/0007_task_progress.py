# Generated by Django 3.2.2 on 2021-09-04 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prjtask', '0006_auto_20210831_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='progress',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]
