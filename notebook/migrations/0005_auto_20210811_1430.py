# Generated by Django 3.2.6 on 2021-08-11 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0004_auto_20210811_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='color',
        ),
        migrations.AlterField(
            model_name='note',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
