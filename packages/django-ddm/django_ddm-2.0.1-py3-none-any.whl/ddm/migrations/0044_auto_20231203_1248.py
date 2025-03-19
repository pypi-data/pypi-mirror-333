# Generated by Django 3.2.13 on 2023-12-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm', '0043_auto_20230525_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='processingrule',
            name='regex_field',
            field=models.BooleanField(default=False, help_text='Select if you use a regex expression in the "Field" setting to match a variable.'),
        ),
        migrations.AlterField(
            model_name='openquestion',
            name='display',
            field=models.CharField(choices=[('small', 'Small'), ('large', 'Large')], default='large', help_text='"Small" displays a one-line textfield, "Large" a multiline textfield as input.', max_length=20),
        ),
    ]
