# Sistema de Gestión de Citas Médicas

Aplicación web desarrollada en **Django** para la gestión integral de citas médicas, pacientes, perfiles y clínicas.

## Estructura del Proyecto

* **`citas/`**: Módulo principal para la programación, modificación y seguimiento de citas médicas.
* **`clínica/`**: Módulo de administración para centros médicos, consultorios y asignación de profesionales.
* **`configuración/`**: Archivos de configuración general del proyecto Django (`settings.py`, `urls.py`, etc.).
* **`perfiles/`**: Gestión de perfiles de usuario y roles dentro del sistema.
* **`usuarios/`**: Autenticación, registro y control de acceso de usuarios.
* **`estático/`**: Archivos estáticos (hojas de estilo CSS, scripts e imágenes).
* **`plantillas/`**: Plantillas HTML de la interfaz de usuario.
* **`gestionar.py`**: Interfaz de línea de comandos para la gestión y ejecución de tareas administrativas (`manage.py`).
* **`requisitos.txt`**: Lista de dependencias y librerías necesarias de Python.
* **`.gitignore`**: Archivos y carpetas excluidas del control de versiones de Git.

## Requisitos Previos

* Python (versión 3.10 o superior recomendada)
* Git

## Instalación y Configuración

1. **Clonar el repositorio:**

   git clone https://github.com/Osias1234/appCitaMedica.git
   cd AppCitasMedicas

2. **Crear y activar el entorno virtual:**

   python -m venv venv
   source venv/Scripts/activate

3. **Instalar las dependencias:**

   pip install -r requisitos.txt

4. **Aplicar las migraciones de la base de datos:**

   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

6. **Ejecutar el servidor de desarrollo:**

   python manage.py runserver

Accede a la aplicación desde tu navegador en http://127.0.0.1:8000/
