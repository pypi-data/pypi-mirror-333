# Generated by Django 3.2.19 on 2023-07-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('degreed2', '0021_auto_20230112_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='degreed2enterprisecustomerconfiguration',
            name='show_course_price',
            field=models.BooleanField(default=False, help_text='Displays course price'),
        ),
        migrations.AddField(
            model_name='historicaldegreed2enterprisecustomerconfiguration',
            name='show_course_price',
            field=models.BooleanField(default=False, help_text='Displays course price'),
        ),
    ]
