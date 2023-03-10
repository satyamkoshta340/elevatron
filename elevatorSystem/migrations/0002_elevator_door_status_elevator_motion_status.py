# Generated by Django 4.0.6 on 2023-02-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevatorSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='elevator',
            name='door_status',
            field=models.CharField(choices=[('open', 'open'), ('close', 'close')], default='close', max_length=5),
        ),
        migrations.AddField(
            model_name='elevator',
            name='motion_status',
            field=models.CharField(choices=[('moving up', 'moving up'), ('moving down', 'moving down'), ('waiting', 'waiting'), ('idle', 'idle')], default='idle', max_length=11),
        ),
    ]
