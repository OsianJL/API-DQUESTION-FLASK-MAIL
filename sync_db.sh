#!/bin/bash
# sync_db.sh
#
# Este script sincroniza tu base de datos PostgreSQL local (en Docker)
# con el backup de la base de datos en Heroku.
#
# Requisitos:
# - Heroku CLI instalada y autenticada.
# - Docker instalado y en ejecución.
# - El contenedor de PostgreSQL debe estar activo.
#
# Configura las siguientes variables según tu entorno:

HEROKU_APP="all-questions-app"        # Nombre de tu app en Heroku
DOCKER_CONTAINER="postgres_container" # Nombre o ID del contenedor de PostgreSQL
DB_USER="admin"                       # Usuario de la base de datos (según tu configuración)
DB_NAME="backend_db"                  # Nombre de la base de datos local en Docker

# En entornos Windows usando Git Bash, es recomendable deshabilitar la conversión automática de rutas:
export MSYS_NO_PATHCONV=1

# Paso 1: Capturar un backup en Heroku
echo "Capturando backup en Heroku..."
heroku pg:backups:capture --app "$HEROKU_APP"

if [ $? -ne 0 ]; then
  echo "Error al capturar el backup en Heroku."
  exit 1
fi

# Paso 2: Descargar el backup
echo "Descargando el backup..."
heroku pg:backups:download --app "$HEROKU_APP"

if [ ! -f latest.dump ]; then
  echo "Error: No se encontró el archivo latest.dump tras la descarga."
  exit 1
fi

# Paso 3: Copiar el backup al contenedor Docker
echo "Copiando latest.dump al contenedor Docker..."
docker cp latest.dump "$DOCKER_CONTAINER":/var/tmp/latest.dump

if [ $? -ne 0 ]; then
  echo "Error al copiar el archivo al contenedor Docker."
  exit 1
fi

# Paso 4: Restaurar el backup en la base de datos local
echo "Restaurando la base de datos en el contenedor Docker..."
docker exec -it "$DOCKER_CONTAINER" pg_restore --verbose --clean --no-acl --no-owner -h localhost -U "$DB_USER" -d "$DB_NAME" /var/tmp/latest.dump

if [ $? -ne 0 ]; then
  echo "Error durante la restauración de la base de datos."
  exit 1
fi

# Paso 5: Borrar el archivo de respaldo local (opcional)
echo "Borrando el archivo local latest.dump..."
rm latest.dump

echo "Proceso completado con éxito."
