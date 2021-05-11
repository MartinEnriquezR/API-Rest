# Backend proyecto terminal
Backend para el funcionamiento del proyecto terminal

## Configuracion
_Crear una base de datos en PostgreSQL_ 
_Configurar las credenciales de la base de datos en el archivo settings.py_
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': <nombre_base_de_datos>,
        'USER': <usuario>,
        'PASSWORD': <password>,
        'HOST': <host>,
        'PORT': <puerto>,
    }
}
```
_Hacer las migraciones necesarias_
```
python maange.py makemigrations
```
_Migrar_
```
python maange.py migrate
```
_Cargar el contenido de los archivos .CSV_
```
python manage.py shell
exec(open('fillModels.py').read())
```

