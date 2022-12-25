# Generated by Django 3.2.16 on 2022-12-24 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20221224_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_profiles', to='base.profile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_profiles', to='base.profile'),
        ),
    ]
