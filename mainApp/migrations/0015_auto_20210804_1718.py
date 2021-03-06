# Generated by Django 3.2.5 on 2021-08-04 12:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0014_auto_20210804_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='analys',
            name='ready',
            field=models.BooleanField(blank=True, default=False, verbose_name='Готовность'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 17, 18, 36, 422549)),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 17, 18, 36, 423550), verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 17, 18, 36, 421551)),
        ),
    ]
