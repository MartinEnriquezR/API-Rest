# Generated by Django 3.1.7 on 2021-04-22 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_remove_alerta_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispositivorastreador',
            name='estado',
        ),
        migrations.AddField(
            model_name='grupo',
            name='estado_alerta',
            field=models.BooleanField(default=False),
        ),
    ]
