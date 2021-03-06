# Generated by Django 3.2 on 2021-08-06 21:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0017_auto_20210807_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время записи'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 2, 27, 0, 525795)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 2, 27, 0, 527792), verbose_name='Дата и время запроса'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 2, 27, 0, 526792), verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 2, 27, 0, 525795)),
        ),
    ]
