# Generated by Django 3.1.7 on 2021-04-23 04:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0003_auto_20210422_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='fecha_hora',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]