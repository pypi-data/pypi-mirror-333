# Generated by Django 4.2.16 on 2024-11-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_datadonation', '0003_auto_20241026_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationinstruction',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
