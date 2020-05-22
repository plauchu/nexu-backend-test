Para la prueba del siguiente código se necesita los siguientes requisitos:

Postgresql  12 con lo siguientes parámetros:
        'NAME': 'Cars',
        'USER': 'postgres',
        'PASSWORD':'test',
        'HOST':'127.0.0.1',
        'PORT':'5432'

Dentro de la carpeta nexus_test crear un ambiente virtual con python y activarlo:
	python -m venv env
	source env/bin/activate

Después debemos instalar las librerías requeridas:
	pip install -r requirements.txt

Se debe ejecutar la migración de los modelos para que se cree la tabla en Postgres:

	python manage.py makemigrations nexu_api
	python manage.py migrate

Esto creará la tabla en postgres sin datos, hay que llenar la tabla para poder continuar.

Para ejecutar el servicio hay que ejecutar la siguiente línea:
python manage.py runserver 0.0.0.0:8000


Para probar la API hay que visitar las siguientes urls:

	http://127.0.0.1:8000/api/brands/
	http://127.0.0.1:8000/api/models/
