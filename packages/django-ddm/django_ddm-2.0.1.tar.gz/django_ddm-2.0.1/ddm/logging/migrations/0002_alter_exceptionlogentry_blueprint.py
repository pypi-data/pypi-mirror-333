# Generated by Django 3.2.13 on 2024-10-25 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_datadonation', '0001_initial'),
        ('ddm_logging', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='exceptionlogentry',
                    name='blueprint',
                    field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ddm_datadonation.donationblueprint'),
                ),
            ],
            # This reuses an existing table, so do nothing.
            database_operations=[],
        )
    ]
