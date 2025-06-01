# NentBook

---

## 1. Para una mejor experiencia...

Sugerimos seguir los siguientes pasos:

1. Lee la documentación del proyecto 'Especificacón de requisitos de software: NentBook' haciendo especial énfasis en el apéndice A 'Manual de usuario'. Familiarizate con la aplicación.


2. Lee la sección 'Acceso a la apliación' de este README y sigue las instrucciones a excepción de la ejecución del servidor.


3. Crea un usuario administrador como se indica en el manual de usuario.


4. Ejecuta el servido y accede con las credenciales del administrador que recién creaste.


5. Crea uno o más grupos dentro de la aplicación.


4. Lee el README que se encuentra en la carpeta src/sql/ 
	- En la base de datos que usaste para este proyecto carga los datos obligatorios del DML.sql
	- Recarga el servidor de NentBook


5. Ya puedes disfutar de NentBook como administrador, ahora puedes crear uuarios sin privilegios directamente desde el servidor.   



## 2. Acceso a la apliación

### Algunos prerequisitos:

* **Conda** (o Miniconda)
* **Docker** (para levantar la BD de PostgreSQL)

### ⚙️ Activación de entorno ⚙️

Crea un entorno y actívalo:

```bash
conda env create --name `nombre del env`
conda activate `nombre del env`
```

A la altura de _environment.yml_ descarga las dependecias necesarias para este proyecto:

```bash
conda env update --file environment.yml --prune
```

*En dado caso de que necesites eliminar el entorno:*

```bash
conda env remove --name `nombre del env`
```

## 🐳 Base de datos 

Si ya tienes PostgreSQL + Docker, debes crear una base de datos llamada `anuario` (o con el nombre que prefieras) y ajustar las credenciales que tiene tu base de datos en `settings.py` dentro de la carpeta `anuario`. Tambien está esta otra guia para más información: [Guía para conectar manualmente BD SQL](Guia%20para%20conectar%20manualmente%20BD%20sql.md)

![Sección a modificar para la Base de Datos local](image.png)

**IMPORTANTE: Asegúrate de que el contenedor de la base de datos esté activo antes de continuar**

##  Migraciones hacia la Base de Datos de postgresql 

Estando a la misma altura que `manage.py` el cual se encuentra en `src/Anuario/manage.py`

Genera y aplica migraciones:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## ▶️ Ejecutar el servidor

```bash
python manage.py runserver
```

Abre luego [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

---


## Extras

* Si se necesita saber mas sobre la conexión y restauración de datos apartir de un .sql puro hacía la BD se puede consular:  
  [Guía para conectar manualmente BD SQL](Guia%20para%20conectar%20manualmente%20BD%20sql.md)

* La estructura de triggers y modelos se encuentra en `app/models.py`.

---

