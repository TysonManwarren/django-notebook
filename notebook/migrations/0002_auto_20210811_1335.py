# Generated by Django 3.2.6 on 2021-08-11 17:35

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='color',
            field=models.CharField(choices=[('a', 'yellow'), ('b', 'white'), ('c', 'green'), ('d', 'red'), ('e', 'blue')], default='a', max_length=1),
        ),
        migrations.AlterField(
            model_name='note',
            name='description',
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=400),
        ),
    ]
