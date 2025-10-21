# Task Management API

## Descripción
La Task Management API es una solución backend robusta y escalable diseñada para gestionar tareas (to-dos) con autenticación de usuarios. Su arquitectura está basada en principios de Clean Architecture y Domain-Driven Design (DDD), garantizando la separación de responsabilidades y facilitando el mantenimiento y expansión del sistema.

### Funcionalidades principales

1.  **Gestión de Usuarios y Autenticación**: Sistema seguro para registro de usuarios y autenticación mediante tokens JWT (JSON Web Token), protegiendo todos los endpoints de tareas.

2.  **CRUD Completo de Tareas**:
    - Crear nuevas tareas con título, descripción y estado
    - Listar todas las tareas
    - Obtener detalles de una tarea específica
    - Actualizar tareas existentes
    - Eliminar tareas

3.  **Validaciones de Dominio**: Sistema robusto de validación mediante Value Objects que garantiza la integridad de los datos:
    - Títulos: 1-200 caracteres
    - Descripciones: opcional, hasta 1000 caracteres
    - Estados: `pending` o `completed`

4.  **Manejo de Errores Estandarizado**: Decoradores personalizados para manejo uniforme de excepciones, proporcionando respuestas consistentes y descriptivas.

**Stack Tecnológico:**
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- JWT para autenticación
- Docker & Docker Compose
- Bcrypt para hashing de contraseñas

---

## Configuración de la API

### Configuración de Variables de Entorno

Antes de ejecutar la aplicación, es necesario configurar las variables de entorno:

1.  Copia el archivo de ejemplo `.env.example` a `.env`:
    ```bash
    cp .env.example .env
    ```

2.  **IMPORTANTE:** Edita el archivo `.env` y cambia `SECRET_KEY` por una clave secreta fuerte y aleatoria para producción.
    ```bash
    # Puedes generar una clave segura con:
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    ```

---

### Inicio Rápido con Docker

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd task_management_api

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar los servicios
docker-compose up --build

# 4. La API estará disponible en:
# - API: http://localhost:8000
# - Documentación Swagger: http://localhost:8000/docs
```

---

### Ejecución con Docker

Para ejecutar la aplicación usando Docker y Docker Compose:

1.  Asegúrate de tener Docker Desktop (o Docker Engine y Docker Compose) instalado en tu sistema.
2.  Navega a la raíz del proyecto en tu terminal.
3.  Para construir la imagen Docker y levantar los servicios:
    ```bash
    docker-compose up --build
    ```
4.  La API estará disponible en `http://localhost:8000`.
5.  La documentación interactiva (Swagger UI) estará en `http://localhost:8000/docs`.
6.  Para detener los contenedores:
    ```bash
    docker-compose down
    ```

---

## Documentación de la API

La documentación completa e interactiva está disponible en **Swagger UI** cuando la aplicación está en ejecución:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

A continuación, se presenta un resumen de los endpoints principales:

---

## Autenticación

### 1. Registrar Usuario

```http
POST /api/v1/auth/register
```

Registra un nuevo usuario en el sistema.

**Cuerpo de la Solicitud:**

```json
{
  "email": "usuario@example.com",
  "username": "usuario123",
  "password": "MiPassword123"
}
```

**Validaciones:**
- `email`: Formato de email válido
- `username`: 3-30 caracteres, solo letras, números, guiones bajos y puntos
- `password`: Mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número

**Respuesta Exitosa (201):**

```json
{
  "message": "User registered successfully. Please verify your email.",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "usuario@example.com",
    "username": "usuario123"
  }
}
```

---

### 2. Login

```http
POST /api/v1/auth/login
```

Inicia sesión y obtiene un token JWT para autenticación.

**Cuerpo de la Solicitud:**

```json
{
  "email": "usuario@example.com",
  "password": "MiPassword123"
}
```

**Respuesta Exitosa (200):**

```json
{
  "message": "Login successful",
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 1800
  }
}
```

---

## Tareas (Tasks)

**NOTA:** Todos los endpoints de tareas requieren autenticación. Incluye el token en el header:
```
Authorization: Bearer <tu_token_jwt>
```

---

### 3. Crear Tarea

```http
POST /api/v1/tasks/
```

Crea una nueva tarea.

**Headers:**
```
Authorization: Bearer <token>
```

**Cuerpo de la Solicitud:**

```json
{
  "title": "Completar documentación",
  "description": "Escribir la documentación completa de la API"
}
```

**Validaciones:**
- `title`: 1-200 caracteres, no puede ser solo espacios
- `description`: Opcional, máximo 1000 caracteres

**Respuesta Exitosa (201):**

```json
{
  "message": "Task registered successfully",
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Completar documentación",
    "description": "Escribir la documentación completa de la API",
    "state": "pending"
  }
}
```

---

### 4. Listar Todas las Tareas

```http
GET /api/v1/tasks/
```

Obtiene todas las tareas del sistema.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta Exitosa (200):**

```json
{
  "message": "Tasks retrieved successfully",
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Completar documentación",
      "description": "Escribir la documentación completa de la API",
      "state": "pending"
    },
    {
      "id": "987fcdeb-51a2-43d7-9abc-123456789def",
      "title": "Revisar código",
      "description": "Code review del PR #123",
      "state": "completed"
    }
  ]
}
```

---

### 5. Obtener Tarea por ID

```http
GET /api/v1/tasks/{task_id}
```

Obtiene los detalles de una tarea específica.

**Headers:**
```
Authorization: Bearer <token>
```

**Parámetros de Ruta:**
- `task_id` (UUID): ID de la tarea

**Respuesta Exitosa (200):**

```json
{
  "message": "Task retrieved successfully",
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Completar documentación",
    "description": "Escribir la documentación completa de la API",
    "state": "pending"
  }
}
```

**Respuesta de Error (404):**

```json
{
  "detail": "Task with id 123e4567-e89b-12d3-a456-426614174000 not found"
}
```

---

### 6. Actualizar Tarea

```http
PUT /api/v1/tasks/{task_id}
```

Actualiza una tarea existente. Todos los campos son opcionales.

**Headers:**
```
Authorization: Bearer <token>
```

**Parámetros de Ruta:**
- `task_id` (UUID): ID de la tarea

**Cuerpo de la Solicitud:**

```json
{
  "title": "Documentación actualizada",
  "description": "Incluir ejemplos de uso",
  "state": "completed"
}
```

**Estados Permitidos:**
- `pending`: Tarea pendiente
- `completed`: Tarea completada

**Respuesta Exitosa (200):**

```json
{
  "message": "Task updated successfully.",
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Documentación actualizada",
    "description": "Incluir ejemplos de uso",
    "state": "completed"
  }
}
```

---

### 7. Eliminar Tarea

```http
DELETE /api/v1/tasks/{task_id}
```

Elimina una tarea del sistema.

**Headers:**
```
Authorization: Bearer <token>
```

**Parámetros de Ruta:**
- `task_id` (UUID): ID de la tarea

**Respuesta Exitosa (200):**

```json
{
  "message": "Task deleted successfully.",
  "task_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o expirado |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## Estructura de Errores

Todos los errores siguen el siguiente formato:

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensaje descriptivo del error",
    "details": "Detalles adicionales (opcional)"
  }
}
```

**Ejemplos de códigos de error:**
- `REQUIRED_FIELD`: Campo requerido faltante
- `INVALID_FORMAT`: Formato de datos inválido
- `INVALID_CREDENTIALS`: Credenciales incorrectas
- `TOKEN_EXPIRED`: Token JWT expirado
- `INVALID_TOKEN`: Token JWT inválido
- `INTERNAL_SERVER_ERROR`: Error interno del servidor

---

## Arquitectura del Proyecto

```
app/
├── auth/                   # Módulo de autenticación
│   ├── application/        # Casos de uso
│   ├── domain/            # Entidades y lógica de negocio
│   └── infrastructure/    # Implementaciones (repos, controllers)
├── task/                  # Módulo de tareas
│   ├── application/       # Casos de uso
│   ├── domain/           # Entidades y lógica de negocio
│   └── infrastructure/   # Implementaciones
├── common/               # Código compartido
└── core/                 # Configuración y utilidades
```

---
