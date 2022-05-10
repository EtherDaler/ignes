# Generated by Django 3.2.5 on 2021-07-18 10:31

from django.db import migrations, models
import django.db.models.deletion
import mainApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Виды анализов',
                'verbose_name_plural': 'Виды анализов',
            },
        ),
        migrations.CreateModel(
            name='ExtraFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название поля')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.analystype', verbose_name='Вид анализов')),
            ],
            options={
                'verbose_name': 'Уникальные поля',
                'verbose_name_plural': 'Уникальные поля',
            },
        ),
        migrations.CreateModel(
            name='MyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('inn', models.BigIntegerField(default=0, verbose_name='ИНН')),
                ('license', models.CharField(max_length=255, verbose_name='Лицензия')),
                ('min_of_just', models.CharField(max_length=255, verbose_name='Министрерство юстиций')),
                ('adress', models.CharField(max_length=255, verbose_name='Адресс')),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Информация о лаборатории',
                'verbose_name_plural': 'Информация о лаборатории',
            },
        ),
        migrations.CreateModel(
            name='Felials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(max_length=255, verbose_name='Адресс')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.myinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraFieldsValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Значение поля')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.extrafields', verbose_name='Поле')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.analystype', verbose_name='Вид анализов')),
            ],
            options={
                'verbose_name': 'Значения уникальных полей',
                'verbose_name_plural': 'Значения уникальных полей',
            },
        ),
        migrations.CreateModel(
            name='ExtraContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='Телефон')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.myinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Analys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_full_name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('person_citizenship', models.CharField(max_length=255, verbose_name='Гражданство')),
                ('person_date_of_birth', models.DateField(default=mainApp.models.default_date, verbose_name='Дата рождения')),
                ('analys_datetime', models.DateTimeField(default=mainApp.models.default_datetime, verbose_name='Дата и время сдачи анализов')),
                ('analys_finish_datetime', models.DateTimeField(default=mainApp.models.default_datetime, verbose_name='Дата и время подготовки анализов')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.analystype', verbose_name='Вид анализов')),
            ],
            options={
                'verbose_name': 'Анализы',
                'verbose_name_plural': 'Анализы',
            },
        ),
    ]
