# Generated by Django 3.2.5 on 2021-08-04 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_auto_20210804_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='analys',
            name='code',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Номер анализов'),
        ),
        migrations.AlterField(
            model_name='answers',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 15, 23, 277114)),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 15, 23, 279109), verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 15, 23, 277114)),
        ),
    ]