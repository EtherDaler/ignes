# Generated by Django 3.2.5 on 2021-08-03 19:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_auto_20210803_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='carusel',
            name='deque',
            field=models.PositiveIntegerField(default=1, verbose_name='Порядок при отображении'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 0, 18, 53, 454324)),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 0, 18, 53, 455323), verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 0, 18, 53, 453324)),
        ),
    ]
