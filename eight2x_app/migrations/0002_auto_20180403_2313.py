# Generated by Django 2.0.3 on 2018-04-03 23:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eight2x_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='option',
            old_name='name',
            new_name='option_name',
        ),
        migrations.RenameField(
            model_name='option',
            old_name='value',
            new_name='option_value',
        ),
        migrations.AddField(
            model_name='user',
            name='lang',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
