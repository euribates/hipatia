# Generated by Django 2.0.4 on 2018-04-22 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archivo', '0002_auto_20180422_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivador',
            name='f_acceso',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AlterField(
            model_name='documento',
            name='f_acceso',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]