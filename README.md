# Trello-POO · Gestión de Proyectos tipo Trello

> Proyecto académico · Programación Orientada a Objetos · INACAP Sede Temuco
> Contexto asignado: **Proyecto 3 – Gestión de Proyectos tipo Trello**
> Docente: Erick Bailey

## Integrantes
- **Halbert Miranda**
- **Benjamin Arriagada**

---

## Descripción general

Aplicación de consola en Python para gestionar proyectos mediante tableros, listas y tarjetas, al estilo de Trello. Está desarrollada con **Programación Orientada a Objetos** y **arquitectura en capas**, usando el ORM **Peewee** sobre **MySQL**. Para usarla hay que iniciar sesión; las contraseñas se ingresan ocultas con **maskpass** y se guardan como hash **bcrypt**.

| Módulo | Qué permite |
|---|---|
| **Acceso** | Iniciar sesión con correo y contraseña, o registrarse |
| **Usuarios** | Registrar, listar, modificar, eliminar (deshabilitar) y volver a habilitar |
| **Proyectos** | Crear, listar, modificar, eliminar, agregar participantes con un rol y ver participantes con sus permisos |
| **Tableros y listas** | Crear el tablero de un proyecto; crear, modificar y eliminar listas; ver el tablero completo |
| **Tarjetas** | Crear, modificar, eliminar, **moverlas entre listas**, **asignar responsables** y cambiar su estado |
| **Comentarios** | Agregar, ver y eliminar comentarios de una tarjeta (el autor es quien inició sesión; solo el autor puede eliminarlo) |
| **Etiquetas** | Crear, ver, modificar y eliminar etiquetas por proyecto; asignarlas y quitarlas de las tarjetas |
| **Reporte de avance** | Porcentaje completado, avance ponderado, tarjetas por estado, carga por responsable y tarjetas vencidas |

### Reglas de negocio
- Para usar la aplicación hay que **iniciar sesión** con correo y contraseña (máximo 3 intentos). Sin autenticación no se accede al menú principal.
- La contraseña debe ser segura: 8 caracteres o más, mayúscula, minúscula, número y un símbolo (@ $ # ! * &).
- Las contraseñas se ingresan ocultas con **maskpass** y se guardan como hash **bcrypt**, nunca en texto plano.
- El **RUT** debe ser válido (dígito verificador, módulo 11) y no puede repetirse. El correo tampoco.
- Quien crea un proyecto queda automáticamente como **administrador**.
- Solo un **administrador** puede agregar participantes o eliminar el proyecto.
- Un usuario no puede participar dos veces en el mismo proyecto.
- Cada proyecto tiene **un solo tablero**.
- Una tarjeta solo puede **moverse entre listas del mismo tablero**.
- El **responsable** de una tarjeta debe **participar en el proyecto** y estar habilitado.
- Estados válidos de una tarjeta: `pendiente`, `en progreso` y `completada`.
- La fecha límite de una tarjeta nueva no puede ser anterior a hoy.
- Una tarjeta está **vencida** si pasó su fecha límite y no está completada.
- No se puede eliminar una lista que todavía tiene tarjetas.
- El RUT de un usuario no se puede modificar.
- El autor de un comentario es el usuario que inició sesión, y **solo el autor** puede eliminarlo.
- Una etiqueta pertenece a un proyecto: su nombre no se repite dentro del proyecto y solo se asigna a tarjetas de ese mismo proyecto.
- Una etiqueta solo se puede eliminar si ninguna tarjeta la está usando.

### Flujo de inicio
```
Aplicación → Login → Validación (correo + contraseña bcrypt) → Menú Principal
```

### Borrado lógico
Los usuarios, proyectos, listas y tarjetas **no se borran** de la base de datos: se marcan con `HABILITADO = 0`. Así se conserva el historial (comentarios, participaciones, tarjetas asignadas) y las claves foráneas no se rompen. Los listados y el reporte muestran solo los registros habilitados. Los comentarios y las etiquetas, que no tienen ese campo, se eliminan de forma física.

### Arquitectura en capas
```
Gestion_proyecto_tello_AP_C2_POO_2/
├── app.py                                  # Punto de entrada
├── Diagrama_Clases_Trello_v4.drawio.png    # Diagrama de clases del dominio (editable)
├── Diagrama_Clases_Trello_v4_capas.png     # Diagrama de clases de las capas
├── Diagrama_Clases_Trello_v4.drawio        # Archivo draw.io con las dos páginas
├── Informe_Diseno_Trello_v6.pdf            # Informe de diseño
├── auxiliares/                             # Mensajes, validaciones, constantes, configuración y funciones auxiliares
│   ├── data_aplicacion.py                  # Nombre, versión, estados, roles y colores válidos
│   ├── entradas.py                         # Lectura segura de textos, números, fechas y confirmaciones
│   ├── menu.py                             # Opciones de los menús
│   ├── mensajes.py                         # Mensajes reutilizables
│   └── validaciones.py                     # Clase Rut, validación de correo y contraseña segura
├── datos/                                  # Persistencia: conexión, modelos ORM, repositorios y scripts SQL
│   ├── conexion.py                         # Conexión usando variables del .env
│   ├── modelos/
│   │   ├── models.py                       # Clases que representan las tablas (ORM Peewee)
│   │   └── dominio.py                      # Estados de tarjeta y roles de proyecto
│   ├── repositorios/                       # Un repositorio por entidad (usuarios, proyectos, tableros, tarjetas, comentarios, etiquetas)
│   └── sql/                                # Scripts de creación, ajustes y datos de prueba
├── negocio/                                # Reglas de negocio y validaciones de procesos
│   ├── servicio_base.py                    # Clase abstracta de todos los servicios
│   └── negocio_*.py                        # Un servicio por entidad
└── presentacion/                           # Interacción con el usuario: login, menús, captura y resultados
    ├── menu.py                             # Clases Menu y MenuPrincipal
    ├── presentacion_sesion.py              # Inicio de sesión
    └── presentacion_*.py                   # Pantallas de cada módulo
```
Cada capa solo se comunica con la de abajo: **presentación → negocio → datos**. Los errores inesperados se capturan en el menú y se muestran sin cerrar la aplicación.

---

## Dependencias

Requisitos del sistema:
- **Python 3.10** o superior
- **MySQL / MariaDB** (por ejemplo, con **XAMPP**)

Librerías de Python (archivo `requirements.txt`):

| Librería | Versión | Para qué se usa |
|---|---|---|
| peewee | 4.5.1 | ORM: modelos y consultas a la base de datos |
| PyMySQL | 1.2.3 | Conector entre Python y MySQL |
| python-decouple | 3.8 | Leer las credenciales desde el archivo `.env` |
| prettytable | 3.18.0 | Mostrar tablas en la consola |
| bcrypt | 5.0.0 | Guardar las contraseñas como hash |
| maskpass | 0.3.7 | Ocultar la contraseña con asteriscos al escribirla |

---

## Procedimiento de instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/halbertmiranda4-cell/Gestion_proyecto_tello_AP_C2_POO_2.git
cd Gestion_proyecto_tello_AP_C2_POO_2
```

### 2. Instalar las librerías
```bash
pip install -r requirements.txt
```

### 3. Configurar el archivo `.env`
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

## Procedimiento de creación de base de datos

Con **XAMPP** encendido (Apache y MySQL), entrar a `http://localhost/phpmyadmin`, abrir la pestaña **SQL** y ejecutar los scripts de `datos/sql/` **en este orden**:

| Orden | Script | Qué hace |
|---|---|---|
| 1 | `Proyecto_Trello.sql` | Crea la base `PROYECTO_TRELLO_V2`, sus tablas y el usuario de MySQL |
| 2 | `2026.10.19_01.00_ajustes_restricciones.sql` | Agrega las restricciones (un tablero por proyecto, estados válidos) |
| 3 | `2026.10.19_21.00_alter_habilitado.sql` | Agrega la columna HABILITADO (borrado lógico) |
| 4 a 12 | `2026.10.19_02.00_insert_usuarios.sql` … `2026.10.19_02.40_insert_comentarios.sql` | Carga los datos de prueba (ejecutarlos en orden) |
| 13 | `2026.11.23_12.00_update_contrasenas.sql` | Solo para bases creadas antes: reemplaza contraseñas en texto plano por hash bcrypt |

Si prefieres usar tu propio usuario de MySQL, créalo así y ponlo en el `.env`:
```sql
CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contrasena';
GRANT ALL PRIVILEGES ON PROYECTO_TRELLO_V2.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

Las reglas principales también están protegidas en la base de datos con restricciones `UNIQUE`, `CHECK` y claves foráneas.

---

## Usuario inicial

Los scripts de prueba crean 4 usuarios con la contraseña guardada como hash bcrypt. Todos usan la misma contraseña de prueba: **`Trello#2026`**.

| Usuario | Correo (para iniciar sesión) | Rol en "Sitio web Cafetería" |
|---|---|---|
| Ana Torres | `ana.torres@trello.cl` | administrador |
| Bruno Díaz | `bruno.diaz@trello.cl` | miembro |
| Carla Muñoz | `carla.munoz@trello.cl` | miembro |
| Diego Rojas | `diego.rojas@trello.cl` | (no participa) |

También se puede crear un usuario nuevo con la opción **Registrarse** de la pantalla de acceso. RUTs válidos de prueba: `22.340.574-6`, `22.450.500-0`, `12.345.678-5`.

Datos de prueba incluidos:
- **"Sitio web Cafetería"**: tablero con 3 listas y 5 tarjetas en distintos estados, incluida una **vencida** y una **sin responsable**, con etiquetas ("Diseño", "Urgente", "Backend") y comentarios.
- **"Sistema de inventario"**: sin tablero, para probar su creación desde la aplicación.

---

## Instrucciones de ejecución

1. Encender **MySQL** en XAMPP.
2. Desde la carpeta del proyecto, ejecutar:
```bash
python app.py
```
3. Iniciar sesión (opción 1) con un correo de la tabla anterior y la contraseña `Trello#2026`:
```
Trello-POO - v1.5.0

--- Acceso ---
[1] - Iniciar sesión
[2] - Registrarse
[0] - Salir
```
4. Se muestra el menú principal:
```
Trello-POO - v1.5.0 · Sesión: Ana Torres
========================================

[1] - Gestión Usuarios
[2] - Gestión Proyectos
[3] - Gestión Tableros y Listas
[4] - Gestión Tarjetas
[5] - Gestión Etiquetas
[6] - Reporte de avance
[0] - Salir
```
5. Los comentarios se manejan desde **Gestión Tarjetas** (opciones 7, 8 y 9) y las etiquetas desde **Gestión Etiquetas**.
6. Para salir de la aplicación, elegir **0**.

---

## Versionado

Se usa versionado semántico **Mayor.Menor.Parche** (Mayor: cambios que rompen la compatibilidad · Menor: nuevas funcionalidades · Parche: correcciones).

| Versión | Cambios |
|---|---|
| v0.1.0 | Estructura en capas y gestión de usuarios |
| v0.2.0 | Gestión de proyectos y participantes |
| v1.0.0 | Tableros, listas, tarjetas y reporte de avance |
| v1.1.0 | Modificar y eliminar (borrado lógico) usuarios, proyectos, listas y tarjetas; captura de errores |
| v1.2.0 | Negocio, repositorios y menú convertidos a clases (abstracción, encapsulamiento, herencia y polimorfismo) |
| v1.3.0 | Herencia de dominio: estados de tarjeta, roles de proyecto y `ElementoTablero` (padre de Lista y Tarjeta); permisos por rol |
| v1.4.0 | Inicio de sesión con correo y contraseña (máximo 3 intentos); validación de contraseña segura; usuarios de prueba con hash bcrypt |
| v1.5.0 | Comentarios y etiquetas: repositorio, servicio y menú propios (CRUD completo); el tablero muestra las etiquetas de cada tarjeta |

---

## Principios de POO aplicados

| Principio | Dónde está | Qué hace |
|---|---|---|
| **Abstracción** | `ServicioBase(ABC)`, `EstadoTarjeta(ABC)`, `RolProyecto(ABC)` | Definen qué deben saber hacer sus hijas, sin decir cómo. No se pueden instanciar. |
| **Encapsulamiento** | `Rut` (`__cuerpo`, `__dv`); `Usuarios.establecer_contrasena()`; `Sesion` (`__usuario`, `__intentos`, `__conectado`); atributos privados de los servicios; `Menu` | Los datos internos son privados y solo se usan mediante métodos y propiedades. La contraseña nunca se asigna directo: siempre se encripta. |
| **Herencia** | Servicios → `ServicioBase`; repositorios → `RepositorioBase` / `RepositorioBorradoLogico`; `Lista` y `Tarjeta` → `ElementoTablero`; estados y roles → sus clases abstractas; `MenuPrincipal(Menu)` | Las clases hijas reutilizan el código del padre. |
| **Polimorfismo** | `eliminar()` en cada servicio; `simbolo()`, `aporte_avance()` y `puede_vencer()` en los estados; permisos en los roles; `nombre`, `tipo()` y `ubicacion()` en Lista y Tarjeta | El mismo método responde distinto según la clase del objeto. Por ejemplo, `eliminar()` deshabilita un usuario, exige que una lista o etiqueta no esté en uso, borra físicamente un comentario o rechaza borrar un tablero. |

### Herencia de dominio

| Jerarquía | Archivo | Polimorfismo |
|---|---|---|
| `EstadoTarjeta` (abstracta) → `Pendiente`, `EnProgreso`, `Completada` | `datos/modelos/dominio.py` | Cada estado redefine `simbolo()`, `aporte_avance()` y `puede_vencer()`. Una tarjeta completada no vence; "en progreso" cuenta como media tarea en el avance ponderado. |
| `RolProyecto` (abstracta) → `Administrador`, `Miembro` | `datos/modelos/dominio.py` | Cada rol redefine `puede_gestionar_participantes()` y `puede_eliminar_proyecto()`. Solo un administrador puede agregar participantes o eliminar el proyecto. |
| `ElementoTablero` → `Lista`, `Tarjeta` | `datos/modelos/models.py` | Comparten `posicion` y `habilitado` (herencia de campos). Cada uno redefine `nombre`, `tipo()` y `ubicacion()`; `resumen()` del padre funciona para ambos. |

---

## Documentación
- Informe de diseño: `Informe_Diseno_Trello_v6.pdf`
- Diagrama de clases del dominio (editable en draw.io): `Diagrama_Clases_Trello_v4.drawio.png`
- Diagrama de clases de las capas: `Diagrama_Clases_Trello_v4_capas.png`
- Archivo draw.io con las dos páginas: `Diagrama_Clases_Trello_v4.drawio` 