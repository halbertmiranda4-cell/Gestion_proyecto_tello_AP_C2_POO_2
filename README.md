# Trello-POO · Gestión de Proyectos tipo Trello

Aplicación de consola en Python para gestionar proyectos mediante tableros, listas y tarjetas, al estilo de Trello. Desarrollada con **Programación Orientada a Objetos** y **arquitectura en capas**, usando el ORM **Peewee** sobre **MySQL**.

> Proyecto académico · Programación Orientada a Objetos · INACAP
> Contexto asignado: **Proyecto 3 – Gestión de Proyectos tipo Trello**

---

## Funcionalidades

| Módulo | Qué permite |
|---|---|
| **Usuarios** | Registrar, listar, modificar, eliminar (deshabilitar) y volver a habilitar |
| **Proyectos** | Crear, listar, modificar, eliminar, agregar participantes con un rol y ver participantes |
| **Tableros y listas** | Crear el tablero de un proyecto; crear, modificar y eliminar listas; ver el tablero completo |
| **Tarjetas** | Crear, modificar, eliminar, **moverlas entre listas**, **asignar responsables** y cambiar su estado |
| **Reporte de avance** | Porcentaje completado, tarjetas por estado, carga por responsable y tarjetas vencidas |

## Reglas de negocio

- El **RUT** debe ser válido (dígito verificador, módulo 11) y no puede repetirse. El correo tampoco.
- Las **contraseñas** se guardan encriptadas con **bcrypt**, nunca en texto plano.
- Quien crea un proyecto queda automáticamente como **administrador**.
- Un usuario no puede participar dos veces en el mismo proyecto.
- Cada proyecto tiene **un solo tablero**.
- Una tarjeta solo puede **moverse entre listas del mismo tablero**.
- El **responsable** de una tarjeta debe **participar en el proyecto** y estar habilitado.
- Estados válidos de una tarjeta: `pendiente`, `en progreso` y `completada`.
- La fecha límite de una tarjeta nueva no puede ser anterior a hoy.
- Una tarjeta está **vencida** si pasó su fecha límite y no está completada.
- No se puede eliminar una lista que todavía tiene tarjetas.
- El RUT de un usuario no se puede modificar.

### Borrado lógico
Los registros **no se borran** de la base de datos: se marcan con `HABILITADO = 0`.
Así se conserva el historial (comentarios, participaciones, tarjetas asignadas) y las claves foráneas no se rompen.
Los listados y el reporte muestran solo los registros habilitados.

Las reglas principales también están protegidas en la base de datos con restricciones `UNIQUE`, `CHECK` y claves foráneas.

---

## Arquitectura en capas

```
Gestion_proyecto_trello/
├── app.py                  # Punto de entrada
├── auxiliares/             # Herramientas compartidas
│   ├── data_aplicacion.py  # Nombre, versión, estados y roles válidos
│   ├── entradas.py         # Lectura segura de textos, números, fechas y confirmaciones
│   ├── menu.py             # Opciones de los menús
│   ├── mensajes.py         # Mensajes reutilizables
│   └── validaciones.py     # Validación de RUT y correo
├── datos/                  # Capa de datos (acceso a MySQL)
│   ├── conexion.py         # Conexión usando variables del .env
│   ├── modelos/models.py   # Clases que representan las tablas (ORM Peewee)
│   ├── repositorios/       # Consultas y guardado por entidad
│   └── sql/                # Scripts de creación, ajustes y datos de prueba
├── negocio/                # Capa de negocio (reglas del sistema)
└── presentacion/           # Capa de presentación (menús de consola)
```

Cada capa solo se comunica con la de abajo: **presentación → negocio → datos**.
Así, las reglas de negocio no dependen de la interfaz y el acceso a datos está centralizado en los repositorios.
Los errores inesperados se capturan en el menú y se muestran sin cerrar la aplicación.

---

## Tecnologías

- Python 3.10 o superior
- MySQL / MariaDB (XAMPP)
- [Peewee](http://docs.peewee-orm.com/): ORM
- PyMySQL: conector para MySQL
- python-decouple: lectura de credenciales desde `.env`
- PrettyTable: tablas en consola
- bcrypt: encriptación de contraseñas
- maskpass: ingreso de contraseñas oculto con asteriscos

---

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/halbertmiranda4-cell/Gestion_proyecto_tello_AP_C2_POO_2.git
cd Gestion_proyecto_tello_AP_C2_POO_2
```

### 2. Instalar las librerías
```bash
pip install -r requirements.txt
```

### 3. Crear la base de datos
Con **XAMPP** encendido (Apache y MySQL), entra a `http://localhost/phpmyadmin` y ejecuta los scripts de `datos/sql/` **en este orden**:

| Orden | Script | Qué hace |
|---|---|---|
| 1 | `Proyecto_Trello.sql` | Crea la base `PROYECTO_TRELLO_V2` y sus tablas |
| 2 | `2026.10.19_01.00_ajustes_restricciones.sql` | Agrega las restricciones (un tablero por proyecto, estados válidos) |
| 3 | `2026.10.19_21.00_alter_habilitado.sql` | Agrega la columna HABILITADO (borrado lógico) |
| 4 a 12 | `2026.10.19_02.00_insert_usuarios.sql` … `2026.10.19_02.40_insert_comentarios.sql` | Carga los datos de prueba (ejecutarlos en orden) |

### 4. Crear un usuario de MySQL para la aplicación
```sql
CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contrasena';
GRANT ALL PRIVILEGES ON PROYECTO_TRELLO_V2.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar el archivo `.env`
Copia `.env.example` con el nombre `.env` y completa tus datos:
```
DB_NAME=PROYECTO_TRELLO_V2
DB_USER=tu_usuario
DB_PASSWORD=tu_contrasena
DB_HOST=localhost
DB_PORT=3306
```
El archivo `.env` **no se sube a GitHub** (está en `.gitignore`), así las credenciales no quedan expuestas.

---

## Ejecución
```bash
python app.py
```

```
Trello-POO - v1.1.0
===================

[1] - Gestión Usuarios
[2] - Gestión Proyectos
[3] - Gestión Tableros y Listas
[4] - Gestión Tarjetas
[5] - Reporte de avance
[0] - Salir
```

## Datos de prueba

Los scripts de prueba crean:
- **4 usuarios**: Ana Torres, Bruno Díaz, Carla Muñoz y Diego Rojas. Ana y Bruno participan en **dos proyectos** (relación muchos a muchos).
- **"Sitio web Cafetería"**: tablero con 3 listas y 5 tarjetas en distintos estados, incluida una **vencida** y una **sin responsable**.
- **"Sistema de inventario"**: sin tablero, para probar su creación desde la aplicación.

RUTs válidos de prueba para registrar usuarios nuevos: `22.340.574-6`, `22.450.500-0`, `12.345.678-5`.

---

## Versionado

Se usa versionado semántico **Mayor.Menor.Parche**:
- **Mayor**: cambios que rompen la compatibilidad (arquitectura, base de datos).
- **Menor**: nuevas funcionalidades.
- **Parche**: correcciones.

| Versión | Cambios |
|---|---|
| v0.1.0 | Estructura en capas y gestión de usuarios |
| v0.2.0 | Gestión de proyectos y participantes |
| v1.0.0 | Tableros, listas, tarjetas y reporte de avance |
| v1.1.0 | Modificar y eliminar (borrado lógico) usuarios, proyectos, listas y tarjetas; captura de errores |

---

## Autor
**Halbert Miranda** · Programación Orientada a Objetos · INACAP
