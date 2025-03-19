# Generated by Django 4.2.14 on 2024-08-22 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0036_auto_20240325_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xblockskilldata',
            name='is_blacklisted',
            field=models.BooleanField(db_index=True, default=False, help_text='Blacklist this xblock skill, useful to handle false positives.'),
        ),
        migrations.AddIndex(
            model_name='xblockskilldata',
            index=models.Index(fields=['created'], name='taxonomy_xb_created_5929ec_idx'),
        ),
    ]
