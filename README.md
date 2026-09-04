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



# Vista general de la página de inicio y autenticación de usuarios
   ## Inicio 
<img width="1358" height="687" alt="image" src="https://github.com/user-attachments/assets/4f5bf9a9-feaf-4795-889f-ee5ccc2a790c" />

  ## autenticacion 
  <img width="1356" height="655" alt="image" src="https://github.com/user-attachments/assets/e06ae7ca-a0be-4f4a-9d9c-8cc3f11cfa9e" />

 ## Panel principal de gestión de citas médicas para el paciente
<img width="1361" height="639" alt="image" src="https://github.com/user-attachments/assets/de3b4228-3328-415d-9266-9de8f8457e08" />

<img width="1360" height="658" alt="image" src="https://github.com/user-attachments/assets/c7a42ceb-79c4-4860-abf4-20330ac2cf27" />

## Formulario de programación y selección de especialidades clínicas
  <img width="1363" height="645" alt="image" src="https://github.com/user-attachments/assets/6e9d1f7d-900b-425e-93d3-be0d08482fa9" />
<img width="1366" height="644" alt="image" src="https://github.com/user-attachments/assets/f806f44b-938f-4337-a83d-6848805152fd" />
<img width="1356" height="650" alt="image" src="https://github.com/user-attachments/assets/7e8b97b1-97b4-48b8-a9e5-8981b4cf16ab" />

## Interfaz de control de centros médicos y consultorios
<img width="1357" height="656" alt="image" src="https://github.com/user-attachments/assets/cb295c32-f5c7-448a-8419-51326311019d" />

## Módulo de administración y control de turnos y horario 
 <img width="1361" height="655" alt="image" src="https://github.com/user-attachments/assets/bfda127c-aa70-4930-88b7-6ea03a61ec8f" />
<img width="1366" height="643" alt="image" src="https://github.com/user-attachments/assets/c615209c-caa6-4d1a-bbd5-fca5089121b0" />


