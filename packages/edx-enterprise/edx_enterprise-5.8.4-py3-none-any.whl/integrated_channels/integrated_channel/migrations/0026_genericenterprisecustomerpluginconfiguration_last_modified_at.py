# Generated by Django 3.2.16 on 2023-01-12 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrated_channel', '0025_auto_20230105_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericenterprisecustomerpluginconfiguration',
            name='last_modified_at',
            field=models.DateTimeField(auto_now=True, help_text='The DateTime of the last change made to this configuration.', null=True),
        ),
    ]
