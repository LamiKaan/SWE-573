# Generated by Django 3.2.16 on 2022-12-17 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20221129_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='link',
            field=models.URLField(null=True),
        ),
    ]
