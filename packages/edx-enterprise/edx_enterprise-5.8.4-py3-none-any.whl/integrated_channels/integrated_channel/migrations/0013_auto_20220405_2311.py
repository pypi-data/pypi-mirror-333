# Generated by Django 3.2.12 on 2022-04-05 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrated_channel', '0012_alter_contentmetadataitemtransmission_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericlearnerdatatransmissionaudit',
            name='enterprise_course_enrollment_id',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='genericlearnerdatatransmissionaudit',
            name='plugin_configuration_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
