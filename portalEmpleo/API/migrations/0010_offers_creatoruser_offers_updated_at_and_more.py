# Generated by Django 4.0.1 on 2022-01-31 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0009_postulation'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='creatorUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creatorUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offers',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='offers',
            name='updaterUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updaterUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
