# Generated by Django 3.2.17 on 2023-02-09 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enterprise', '0166_auto_20221209_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterpriseCourseEntitlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('course_uuid', models.CharField(help_text='The UUID of the course (not course run) in which the learner is entitled.', max_length=255)),
                ('enterprise_customer_user', models.ForeignKey(help_text='The enterprise learner to which this entitlement is attached.', on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_entitlements', to='enterprise.enterprisecustomeruser')),
            ],
            options={
                'ordering': ['created'],
                'unique_together': {('enterprise_customer_user', 'course_uuid')},
            },
        ),
        migrations.CreateModel(
            name='HistoricalEnterpriseCourseEntitlement',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('course_uuid', models.CharField(help_text='The UUID of the course (not course run) in which the learner is entitled.', max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('enterprise_customer_user', models.ForeignKey(blank=True, db_constraint=False, help_text='The enterprise learner to which this entitlement is attached.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='enterprise.enterprisecustomeruser')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical enterprise course entitlement',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LearnerCreditEnterpriseCourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=False)),
                ('fulfillment_type', models.CharField(choices=[('license', 'License'), ('learner_credit', 'Learner credit'), ('coupon_code', 'Coupon code')], default='license', help_text="Subsidy fulfillment type, can be one of: ['license', 'learner_credit', 'coupon_code']", max_length=128)),
                ('is_revoked', models.BooleanField(default=False, help_text="Whether the enterprise subsidy is revoked, e.g., when a user's license is revoked.")),
                ('transaction_id', models.UUIDField(editable=False)),
                ('enterprise_course_enrollment', models.OneToOneField(blank=True, help_text='The course enrollment the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learnercreditenterprisecourseenrollment_enrollment_fulfillment', to='enterprise.enterprisecourseenrollment')),
                ('enterprise_course_entitlement', models.OneToOneField(blank=True, help_text='The course entitlement the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learnercreditenterprisecourseenrollment_entitlement_fulfillment', to='enterprise.enterprisecourseentitlement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='licensedenterprisecourseenrollment',
            name='fulfillment_type',
            field=models.CharField(choices=[('license', 'License'), ('learner_credit', 'Learner credit'), ('coupon_code', 'Coupon code')], default='license', help_text="Subsidy fulfillment type, can be one of: ['license', 'learner_credit', 'coupon_code']", max_length=128),
        ),
        migrations.AddField(
            model_name='licensedenterprisecourseenrollment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=False),
        ),
        migrations.AlterField(
            model_name='licensedenterprisecourseenrollment',
            name='enterprise_course_enrollment',
            field=models.OneToOneField(blank=True, help_text='The course enrollment the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='licensedenterprisecourseenrollment_enrollment_fulfillment', to='enterprise.enterprisecourseenrollment'),
        ),
        migrations.AlterField(
            model_name='licensedenterprisecourseenrollment',
            name='is_revoked',
            field=models.BooleanField(default=False, help_text="Whether the enterprise subsidy is revoked, e.g., when a user's license is revoked."),
        ),
        migrations.AddField(
            model_name='historicallicensedenterprisecourseenrollment',
            name='enterprise_course_entitlement',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The course entitlement the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='enterprise.enterprisecourseentitlement'),
        ),
        migrations.AddField(
            model_name='historicallicensedenterprisecourseenrollment',
            name='fulfillment_type',
            field=models.CharField(choices=[('license', 'License'), ('learner_credit', 'Learner credit'), ('coupon_code', 'Coupon code')], default='license', help_text="Subsidy fulfillment type, can be one of: ['license', 'learner_credit', 'coupon_code']", max_length=128),
        ),
        migrations.AddField(
            model_name='historicallicensedenterprisecourseenrollment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='historicallicensedenterprisecourseenrollment',
            name='enterprise_course_enrollment',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='The course enrollment the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='enterprise.enterprisecourseenrollment'),
        ),
        migrations.AlterField(
            model_name='historicallicensedenterprisecourseenrollment',
            name='is_revoked',
            field=models.BooleanField(default=False, help_text="Whether the enterprise subsidy is revoked, e.g., when a user's license is revoked."),
        ),
        migrations.CreateModel(
            name='HistoricalLearnerCreditEnterpriseCourseEnrollment',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, null=True)),
                ('fulfillment_type', models.CharField(choices=[('license', 'License'), ('learner_credit', 'Learner credit'), ('coupon_code', 'Coupon code')], default='license', help_text="Subsidy fulfillment type, can be one of: ['license', 'learner_credit', 'coupon_code']", max_length=128)),
                ('is_revoked', models.BooleanField(default=False, help_text="Whether the enterprise subsidy is revoked, e.g., when a user's license is revoked.")),
                ('transaction_id', models.UUIDField(editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('enterprise_course_enrollment', models.ForeignKey(blank=True, db_constraint=False, help_text='The course enrollment the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='enterprise.enterprisecourseenrollment')),
                ('enterprise_course_entitlement', models.ForeignKey(blank=True, db_constraint=False, help_text='The course entitlement the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='enterprise.enterprisecourseentitlement')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical learner credit enterprise course enrollment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='licensedenterprisecourseenrollment',
            name='enterprise_course_entitlement',
            field=models.OneToOneField(blank=True, help_text='The course entitlement the associated subsidy is for.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='licensedenterprisecourseenrollment_entitlement_fulfillment', to='enterprise.enterprisecourseentitlement'),
        ),
    ]
