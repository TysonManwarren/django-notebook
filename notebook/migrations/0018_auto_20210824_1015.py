# Generated by Django 3.2.6 on 2021-08-24 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0017_alter_note_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='note',
            name='version',
        ),
    ]
