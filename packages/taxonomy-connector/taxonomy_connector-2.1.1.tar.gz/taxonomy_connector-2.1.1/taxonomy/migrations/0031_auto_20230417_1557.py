# Generated by Django 3.2.18 on 2023-04-17 15:57

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0030_alter_skillsquiz_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(default='', help_text='AI generated job description.'),
        ),
        migrations.CreateModel(
            name='JobPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.TextField(help_text='AI generated current job to future job path description.')),
                ('current_job', models.ForeignKey(help_text='The external id of the current job.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='taxonomy.job', to_field='external_id')),
                ('future_job', models.ForeignKey(help_text='The external id of the future job.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='taxonomy.job', to_field='external_id')),
            ],
            options={
                'ordering': ('created',),
                'unique_together': {('current_job', 'future_job')},
            },
        ),
    ]
