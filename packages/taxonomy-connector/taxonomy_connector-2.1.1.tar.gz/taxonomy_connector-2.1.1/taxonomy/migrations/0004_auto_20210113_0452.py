# Generated by Django 2.2.17 on 2021-01-13 04:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_auto_20200916_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobskills',
            name='name',
        ),

        migrations.AddField(
            model_name='jobskills',
            name='skill',
            field=models.ForeignKey(help_text='The skill required for the job.', on_delete=django.db.models.deletion.CASCADE, to='taxonomy.Skill'),
            preserve_default=False,
        ),
    ]
