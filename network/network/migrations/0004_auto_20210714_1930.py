# Generated by Django 3.2.2 on 2021-07-15 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20210714_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follower_no',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_no',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
