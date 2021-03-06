# Generated by Django 3.2 on 2021-08-08 20:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0020_auto_20210809_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=512, verbose_name='ФИО')),
                ('photo', models.ImageField(upload_to='crew', verbose_name='Фотография')),
                ('instagram', models.CharField(blank=True, max_length=255, verbose_name='Ссылка на Instagram')),
                ('facebook', models.CharField(max_length=255, verbose_name='Ссылка на facebook')),
                ('telegram', models.CharField(max_length=255, verbose_name='Имя в телеграмм')),
                ('about', models.TextField(verbose_name='О сотруднике')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('education', models.CharField(max_length=512, verbose_name='Образование')),
            ],
            options={
                'verbose_name': 'Персонал',
                'verbose_name_plural': 'Персонал',
            },
        ),
        migrations.AlterField(
            model_name='answers',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 9, 1, 57, 25, 259475)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 9, 1, 57, 25, 260475), verbose_name='Дата и время запроса'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 9, 1, 57, 25, 260475), verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 9, 1, 57, 25, 258469)),
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=255, verbose_name='Место работы')),
                ('period', models.CharField(max_length=255, verbose_name='Период работы')),
                ('crew', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='mainApp.crew', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Опыт работы',
                'verbose_name_plural': 'Опыт работы',
            },
        ),
    ]
