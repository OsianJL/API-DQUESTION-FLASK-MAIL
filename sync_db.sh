#!/bin/bash
# sync_db.sh
# Script para sincronizar la base de datos local (Docker) con la base de datos de Heroku.

HEROKU_APP="all-questions-app"        # Nombre de tu app en Heroku
DOCKER_CONTAINER="postgres_container" # Nombre o ID del contenedor de PostgreSQL
DB_USER="admin"                       # Usuario de la base de datos
DB_NAME="backend_db"                  # Nombre de la base de datos local

# Deshabilitar la conversión automática de rutas en Git Bash (si es necesario)
export MSYS_NO_PATHCONV=1

echo "Capturando backup en Heroku..."
heroku pg:backups:capture --app "$HEROKU_APP"

if [ $? -ne 0 ]; then
  echo "Error al capturar el backup en Heroku."
  exit 1
fi

echo "Descargando el backup..."
heroku pg:backups:download --app "$HEROKU_APP"

if [ ! -f latest.dump ]; then
  echo "Error: No se encontró el archivo latest.dump tras la descarga."
  exit 1
fi

echo "Copiando latest.dump al contenedor Docker..."
docker cp latest.dump "$DOCKER_CONTAINER":/var/tmp/latest.dump

if [ $? -ne 0 ]; then
  echo "Error al copiar el archivo al contenedor Docker."
  exit 1
fi

echo "Restaurando la base de datos en el contenedor Docker..."
# Se ignoran los errores no críticos usando "|| true"
docker exec -it "$DOCKER_CONTAINER" pg_restore --verbose --clean --no-acl --no-owner -h localhost -U "$DB_USER" -d "$DB_NAME" /var/tmp/latest.dump || true

if [ $? -ne 0 ]; then
  echo "Advertencia: Se produjeron errores durante la restauración (que pueden ser ignorables)."
fi

echo "Borrando el archivo local latest.dump..."
rm latest.dump

echo "Proceso completado con éxito."
