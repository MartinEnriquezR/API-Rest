#!/usr/bin/env python

"""
    Script to import data from .csv file to Model Database DJango
    To execute this script run: 
        1) manage.py shell
        2) exec(open('fillModels.py').read())
"""
import csv
from catalogo.models import *

path = 'ModelosCSV/Circunstancia.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        Circunstancia.objects.create(tipo_circunstancia=row[0])

path = 'ModelosCSV/ColorCabello.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        ColorCabello.objects.create(color_cabello=row[0])

path = 'ModelosCSV/ColorOjos.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        ColorOjos.objects.create(color_ojo=row[0])

path = 'ModelosCSV/ColorPiel.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        ColorPiel.objects.create(color_piel= row[0])

path = 'ModelosCSV/Complexion.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        Complexion.objects.create(complexion= row[0])

path = 'ModelosCSV/Enfermedad.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        Enfermedad.objects.create(nombre_enfermedad=row[0])

path = 'ModelosCSV/FormaRostro.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        FormaRostro.objects.create(forma_rostro=row[0])

path = 'ModelosCSV/Lazo.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        Lazo.objects.create(lazo=row[0])

path = 'ModelosCSV/Pais.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        Pais.objects.create(nombre_pais=row[0],nacionalidad=row[1])

path = 'ModelosCSV/SenasParticulares.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        SenasParticulares.objects.create(nombre_sena_particular=row[0])

path = 'ModelosCSV/TexturaCabello.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        TexturaCabello.objects.create(textura_cabello = row[0])

path = 'ModelosCSV/TipoCejas.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        TipoCejas.objects.create(tipo_ceja=row[0])

path = 'ModelosCSV/TipoNariz.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        TipoNariz.objects.create(tipo_nariz=row[0])

path = 'ModelosCSV/UbicacionCorporal.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        UbicacionCorporal.objects.create(nombre_ubicacion_corporal=row[0])

path = 'ModelosCSV/EstadoCivil.csv'
with open(path) as csvfile:
    campos = csv.reader(csvfile,delimiter=',')
    for row in campos:
        EstadoCivil.objects.create(estado_civil=row[0])