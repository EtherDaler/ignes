# Generated by Django 3.2.5 on 2021-08-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_auto_20210729_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='analystype',
            name='logo',
            field=models.ImageField(default='probirka.png', upload_to='analys_types', verbose_name='Лого'),
        ),
    ]
