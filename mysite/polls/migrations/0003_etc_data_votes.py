# Generated by Django 2.2.6 on 2019-10-29 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_etc_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='etc_data',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]