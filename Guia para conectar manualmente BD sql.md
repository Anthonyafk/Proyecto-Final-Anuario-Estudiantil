### Verificamos nuestros contenedores de Docker

- Verificamos los contenedores disponibles en Docker utilizando el comando:

```bash
docker ps -a
```
Esto nos muestra los contenedores en ejecución y detenidos. Si ya tenemos un contenedor de PostgreSQL creado, lo podemos localizar con su `CONTAINER ID` o `NAME`.


### 2. Iniciar o crear un contenedor con PostgreSQL (si no tenemos uno xd)

Si no tenemos ninguno, puedemos crear uno nuevo con el siguiente comando:

```bash
docker run --name mi_postgres -e POSTGRES_PASSWORD=mi_contraseña -p 5432:5432 -d postgres
```

Esto creará un contenedor llamado `mi_postgres` con la contraseña `mi_contraseña` para el usuario `postgres`.

Para iniciarlo en caso de ya tengamos uno es con:

```bash
sudo docker start <ID del contenedor>
```

---

### 3. Conectarse al contenedor PostgreSQL

Una vez que el contenedor esté en ejecución, podemos acceder a la consola de PostgreSQL con:

```bash
docker exec -it <ID del contenedor> psql -U postgres
```

Una vez dentro, puedes verificar las bases de datos existentes con:

```sql
\l
```

Y salir con:

```sql
\q
```

---


### 4. Crear una base de datos nueva (desde fuera del contenedor)

Para crear una nueva base de datos (por ejemplo, `anuario`), puedemos usar:

```bash
docker exec -it <ID del contenedor> createdb -U postgres anuario
```

Después, puedes conectarte a ella con:

```bash
docker exec -it <ID del contenedor> psql -U postgres -d anuario
```

Y ver que tablas tiene con:

```sql
\dt
```


*Desde adentro del contenedor se realiza con:*

```bash
CREATE DATABASE nombredelaDB;
```

*Para conectarse desde adentro es con:*

```bash
\c nombredelaBD;
```

---

### 5. Restaurar una base de datos desde un archivo 

**(Aviso: Esto solo es para el archivo DB_Anuario.sql, para tener cargada la base con Django es otro procedimiento que detallare mas adelante, pero probablemente no sea necesario que todos lo hagan, con que se haga una vez puede que sea suficiente :v)**

Para restaurar una base de datos desde el archivo nos aseguramos primero de que la base de datos exista y esté vacía.


Luego, ejecutamos el siguiente comando (ajustando las rutas y nombres según tu caso):

```bash
docker exec -i <id contenedor> psql -U postgres -d anuario <  home.../ruta/al/archivo/DB_Anuario.sql
```

postgres = usuario

anuario = bd

---

### 6. Verificamos que la restauración fue exitosa

Después de la restauración, puedes conectarte a la base de datos y revisar sus tablas con:

```bash
docker exec -it <ID del contenedor> psql -U postgres -d anuario
```

Dentro de `psql`:

```sql
\dt
```

y ya se debería de ver listadas las tablas restauradas.


### Para borrar una BD

Desde fuera de docker se puede hacer con:

```
docker exec -it <ID del contenedor> dropdb -U postgres <nombre de la BD>
```
