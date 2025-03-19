# Generated by Django 4.2.16 on 2024-12-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm_projects', '0002_alter_donationproject_briefing_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationproject',
            name='active',
            field=models.BooleanField(default=True, help_text='Participants can only take part in a project if it is active.', verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='donationproject',
            name='redirect_target',
            field=models.CharField(blank=True, help_text='Always include <i>http://</i> or <i>https://</i> in the redirect address. If URL parameter extraction is enabled for this project, you can include the extracted URL parameters in the redirect address as follows: "https://redirect.me/?redirectpara=<b>{{participant.data.url_param.URLParameter}}</b>".', max_length=2000, verbose_name='Redirect address'),
        ),
        migrations.AlterField(
            model_name='donationproject',
            name='slug',
            field=models.SlugField(help_text='Identifier that is included in the URL through which participants can access the project (e.g, https://root.url/url-identifier). Can only contain letters, hyphens, numbers or underscores.', unique=True, verbose_name='URL Identifier'),
        ),
    ]
