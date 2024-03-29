# Generated by Django 3.1.7 on 2021-04-19 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circunstancia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_circunstancia', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'CIRCUNSTANCIA',
            },
        ),
        migrations.CreateModel(
            name='ColorCabello',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_cabello', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'COLOR_CABELLO',
            },
        ),
        migrations.CreateModel(
            name='ColorOjos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_ojo', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'COLOR_OJOS',
            },
        ),
        migrations.CreateModel(
            name='ColorPiel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_piel', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'COLOR_PIEL',
            },
        ),
        migrations.CreateModel(
            name='Complexion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complexion', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'COMPLEXION',
            },
        ),
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_enfermedad', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ENFERMEDAD',
            },
        ),
        migrations.CreateModel(
            name='EstadoCivil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_civil', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ESTADO_CIVIL',
            },
        ),
        migrations.CreateModel(
            name='FormaRostro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_rostro', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'FORMA_ROSTRO',
            },
        ),
        migrations.CreateModel(
            name='Lazo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lazo', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'LAZO',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_pais', models.CharField(max_length=30)),
                ('nacionalidad', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'PAIS',
            },
        ),
        migrations.CreateModel(
            name='SenasParticulares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sena_particular', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'SENAS_PARTICULARES',
            },
        ),
        migrations.CreateModel(
            name='TexturaCabello',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textura_cabello', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TEXTURA_CABELLO',
            },
        ),
        migrations.CreateModel(
            name='TipoCejas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ceja', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'TIPO_CEJAS',
            },
        ),
        migrations.CreateModel(
            name='TipoNariz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_nariz', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TIPO_NARIZ',
            },
        ),
        migrations.CreateModel(
            name='UbicacionCorporal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ubicacion_corporal', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'UBICACION_CORPORAL',
            },
        ),
    ]
