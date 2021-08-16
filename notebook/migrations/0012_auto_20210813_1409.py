# Generated by Django 3.2.6 on 2021-08-13 18:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0011_auto_20210813_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['display_order']},
        ),
        migrations.AlterModelOptions(
            name='notebook',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='note',
            old_name='timestamp',
            new_name='created_timestamp',
        ),
        migrations.RemoveField(
            model_name='note',
            name='date',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='notebooktab',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='note',
            name='modified_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='note',
            name='display_order',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='indent',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
    ]