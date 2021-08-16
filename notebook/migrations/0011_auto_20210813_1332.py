# Generated by Django 3.2.6 on 2021-08-13 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0010_auto_20210812_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='tag',
        ),
        migrations.AddField(
            model_name='note',
            name='display_order',
            field=models.IntegerField(default=0, editable=False, max_length=10),
        ),
        migrations.AddField(
            model_name='note',
            name='indent',
            field=models.SmallIntegerField(default=0, editable=False, max_length=1),
        ),
        migrations.DeleteModel(
            name='NotebookPage',
        ),
    ]