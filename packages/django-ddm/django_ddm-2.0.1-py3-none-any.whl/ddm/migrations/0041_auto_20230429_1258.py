# Generated by Django 3.2.13 on 2023-04-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm', '0040_participant_current_step'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='questionitem',
            constraint=models.UniqueConstraint(fields=('index', 'question'), name='unique_item_index_per_question'),
        ),
        migrations.AddConstraint(
            model_name='questionitem',
            constraint=models.UniqueConstraint(fields=('value', 'question'), name='unique_item_value_per_question'),
        ),
    ]
