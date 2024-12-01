# Minerva - Backend para Gestión de Tareas

Minerva es una API desarrollada con **FastAPI** para gestionar tareas de manera eficiente. Proporciona funcionalidad CRUD para tareas y cuenta con un sistema de autenticación basado en JWT, incluyendo control de acceso según el rol del usuario.

## Características

- **CRUD de tareas**: 
  - Crear, leer, actualizar y eliminar tareas.
  - Cada tarea incluye:
    - Título (obligatorio).
    - Descripción (opcional).
    - Usuario asignado.

- **Autenticación**:
  - Basada en JWT.
  - Registro e inicio de sesión de usuarios.

- **Control de acceso**:
  - Protege rutas según el rol del usuario (e.g., administrador, usuario estándar).
