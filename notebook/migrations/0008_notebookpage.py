# Generated by Django 3.2.6 on 2021-08-12 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0007_auto_20210812_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotebookPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('notebook_tab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='notebook.notebooktab')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
