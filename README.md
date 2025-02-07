I'll convert the README to a clean, well-formatted Markdown document.





# Backend Test API

Esta API es un proyecto de ejemplo que utiliza las siguientes tecnologías:

- **Python 3.11+**
- **Flask** (con Flask-RESTful para los endpoints)
- **Flask-SQLAlchemy** para la gestión de la base de datos
- **Flask-Migrate** para las migraciones
- **Flask-Admin** para la interfaz administrativa
- **Flask-JWT-Extended** para la autenticación basada en JWT
- **bcrypt** para el hashing de contraseñas
- **Docker** para ejecutar PostgreSQL localmente
- **Heroku** para el despliegue en producción

La API permite registrar usuarios, iniciar sesión (retornando un token JWT) y acceder a rutas protegidas. Además, dispone de un panel de administración para gestionar los usuarios.

---

## Estructura del Proyecto

```plaintext
backend-test-00/
├── app/
│   ├── models/
│   │   └── user.py         # Modelo User (se define __tablename__ = "users")
│   ├── resources/
│   │   ├── auth.py         # Endpoints de registro y login
│   │   └── protected.py    # Endpoint protegido (requiere token JWT)
│   ├── services/           # Lógica adicional (e.g., validaciones)
│   ├── __init__.py         # Función create_app() y configuración de extensiones
│   ├── config.py           # Configuración (carga .env, DATABASE_URL, JWT_SECRET_KEY)
│   └── extensions.py       # Inicialización de db, bcrypt, jwt, etc.
├── migrations/             # Migraciones generadas por Flask-Migrate
├── tests/                  # Pruebas unitarias e integración
├── docker-compose.yml      # Configuración de Docker para PostgreSQL
├── requirements.txt        # Lista de dependencias
├── run.py                  # Punto de entrada de la API
├── sync_db.sh              # Script para sincronizar la base de datos con Heroku
└── README.md               # Este archivo
```

## Configuración Local

### 1. Clonar y preparar el entorno

Clona el repositorio:

```bash
git clone <URL-del-repositorio>
cd backend-test-00
```

Crea un entorno virtual y actívalo:

```bash
# En Linux/macOS:
python3.11 -m venv venv
source venv/bin/activate

# En Windows (cmd):
python3.11 -m venv venv
venv\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (ajusta los valores según necesites):

```ini
DATABASE_URL=postgresql://admin:adminpassword@localhost:5432/backend_db
JWT_SECRET_KEY=tu_clave_secreta_segura
```

### 3. Levantar PostgreSQL con Docker

Si utilizas Docker y tienes configurado un archivo `docker-compose.yml` similar al siguiente:

```yaml
version: '3.8'
services:
  db:
    image: postgres:16
    container_name: postgres_container
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: adminpassword
      POSTGRES_DB: backend_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Levanta el contenedor:

```bash
docker-compose up -d
```

### 4. Aplicar Migraciones

Con la base de datos configurada y el entorno activado, ejecuta:

```bash
flask db upgrade
```

Esto creará las tablas necesarias en la base de datos local (por ejemplo, la tabla users).

### 5. Ejecutar la API en Local

Inicia la API:

```bash
python run.py
```

La API se ejecutará en http://127.0.0.1:5000.
El panel de administración estará disponible en http://127.0.0.1:5000/admin.

## Despliegue en Heroku

### 1. Preparar el entorno para Heroku

**Procfile**: Asegúrate de tener un archivo `Procfile` en la raíz con:

```
web: gunicorn run:app
```

**.python-version**: Crea un archivo `.python-version` (en lugar de `runtime.txt`) con el contenido:

```
3.11
```

### 2. Configurar la aplicación en Heroku

Inicia sesión en Heroku CLI:

```bash
heroku login
```

Crea la aplicación (o usa una existente):

```bash
heroku create all-questions-app
```

Agrega el add-on de PostgreSQL:

```bash
heroku addons:create heroku-postgresql --plan essential-0 --app all-questions-app
```

Configura las variables de entorno en Heroku:

```bash
heroku config:set JWT_SECRET_KEY="tu_clave_secreta_segura" --app all-questions-app
```

### 3. Desplegar el Código

Asegúrate de que todos los cambios estén confirmados en Git:

```bash
git add .
git commit -m "Preparar despliegue en Heroku"
```

Envía el código a Heroku:

```bash
git push heroku main
```

Ejecuta las migraciones en Heroku:

```bash
heroku run flask db upgrade --app all-questions-app
```

Abre la aplicación en Heroku:

```bash
heroku open --app all-questions-app
```

## Sincronización de la Base de Datos desde Heroku a Local

Se ha creado el script `sync_db.sh` para automatizar el siguiente proceso:

- Capturar un backup de la base de datos en Heroku.
- Descargar el backup como `latest.dump`.
- Copiar el backup al contenedor Docker.
- Restaurar el backup en la base de datos local.
- Borrar el archivo de respaldo local.

### Cómo usar el script

Asegúrate de tener Docker y Heroku CLI instalados y configurados.

Desde la raíz del proyecto, haz ejecutable el script (si no lo está):

```bash
chmod +x sync_db.sh
```

Ejecuta el script:

```bash
./sync_db.sh
```

> **Nota**: El script sobrescribe la base de datos local (`backend_db`) con los datos de Heroku. Asegúrate de no tener datos importantes en local o respáldalos antes.

## Uso de la API

### Registro: POST `/register`

Cuerpo JSON:

```json
{
  "email": "usuario@example.com",
  "password": "Clave@1234"
}
```

### Login: POST `/login`

Cuerpo JSON:

```json
{
  "email": "usuario@example.com",
  "password": "Clave@1234"
}
```

Se recibe un token JWT en la respuesta.

### Ruta protegida: GET `/protected`

Incluye la cabecera:

```
Authorization: Bearer <tu_token>
```

### Panel de administración: GET `/admin`

Se accede a través del navegador para gestionar usuarios (la contraseña no se muestra, ya que se oculta en la vista).

## Notas Adicionales

- **JWT y Seguridad**: La API utiliza JWT para la autenticación y bcrypt para almacenar contraseñas de forma segura.
- **Migraciones**: Si realizas cambios en el modelo, recuerda generar y aplicar nuevas migraciones con:

  ```bash
  flask db migrate -m "Mensaje de migración"
  flask db upgrade
  ```

- **Docker**: Asegúrate de que el contenedor de PostgreSQL esté usando una versión compatible (en este proyecto se ha sincronizado la versión en Heroku y local, por ejemplo, PostgreSQL 16).

## Problemas Comunes y Solución

### Error "relation 'user' does not exist"

Asegúrate de que el modelo User tenga definido `__tablename__ = "users"` para evitar conflictos con la palabra reservada "user", y que las migraciones se hayan aplicado correctamente.

### Problemas al sincronizar la base de datos

Revisa que la variable `MSYS_NO_PATHCONV=1` esté establecida si usas Git Bash en Windows, para evitar conversiones de ruta que afecten los comandos de Docker.

## Licencia

Este proyecto es de código abierto y se distribuye bajo [tu licencia preferida] (por ejemplo, MIT License).

¡Listo! Con este README tendrás una guía completa para levantar la API en local, desplegarla en Heroku, y sincronizar la base de datos cuando sea necesario.


Here's the Markdown version of your README. I've maintained the original structure, formatting, and content while converting it to a clean Markdown format. The code blocks are preserved, and the overall readability is enhanced. Would you like me to make any specific adjustments?