#!/bin/bash
# Entrypoint script for Django container

set -e

echo "Esperando a que PostgreSQL esté listo..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL está listo!"

# Run migrations
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Collect static files
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Verificando superusuario..."
python manage.py shell <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@calculadora.local', 'admin')
    print('Superusuario creado: admin / admin')
else:
    print('Superusuario ya existe')
END

echo "Iniciando servidor Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile -
