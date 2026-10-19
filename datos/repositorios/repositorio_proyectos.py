from peewee import fn, JOIN, IntegrityError, OperationalError, DataError, PeeweeException
from datos.modelos.models import database, Proyecto, UsuarioProyecto, Usuarios


def listado_proyectos():
    # Cada proyecto con la cantidad de participantes (LEFT JOIN para incluir proyectos sin participantes)
    proyectos = (Proyecto
                 .select(Proyecto, fn.COUNT(UsuarioProyecto.id_usuario_proyecto).alias('participantes'))
                 .join(UsuarioProyecto, JOIN.LEFT_OUTER, on=(UsuarioProyecto.id_proyecto == Proyecto.id_proyecto))
                 .group_by(Proyecto.id_proyecto)
                 .order_by(Proyecto.id_proyecto))
    if proyectos:
        return proyectos


def buscar_proyecto_por_id(id_proyecto: int):
    return Proyecto.get_or_none(Proyecto.id_proyecto == id_proyecto)


def buscar_proyecto_por_nombre(nombre: str):
    return Proyecto.get_or_none(Proyecto.nompro == nombre)


def buscar_participacion(usuario: Usuarios, proyecto: Proyecto):
    return UsuarioProyecto.get_or_none(
        (UsuarioProyecto.id_usuario == usuario) & (UsuarioProyecto.id_proyecto == proyecto))


def listado_participantes(proyecto: Proyecto):
    participantes = (UsuarioProyecto
                     .select(UsuarioProyecto, Usuarios)
                     .join(Usuarios, on=(UsuarioProyecto.id_usuario == Usuarios.id_usuario))
                     .where(UsuarioProyecto.id_proyecto == proyecto)
                     .order_by(UsuarioProyecto.rol, Usuarios.nombre))
    if participantes:
        return participantes


def guardar_proyecto_con_administrador(proyecto: Proyecto, usuario: Usuarios) -> bool:
    # atomic(): se guardan el proyecto y su administrador juntos, o no se guarda nada
    try:
        with database.atomic():
            proyecto.save()
            UsuarioProyecto.create(id_usuario=usuario, id_proyecto=proyecto, rol='administrador')
        print(f'Proyecto guardado con éxito con Id: {proyecto.id_proyecto}.')
        return True
    except IntegrityError as e:
        print(f'Error de clave única o clave foránea: {e}')
    except OperationalError as e:
        print(f'Error operacional\n(pérdida de conexión, falta una tabla o base de datos bloqueada): {e}')
    except DataError as e:
        print(f'Valor insertado NO corresponde: {e}')
    except PeeweeException as e:
        print(f'No se pudieron guardar los datos por un error genérico: {e}')
    return False


def guardar_participante(usuario: Usuarios, proyecto: Proyecto, rol: str) -> bool:
    try:
        UsuarioProyecto.create(id_usuario=usuario, id_proyecto=proyecto, rol=rol)
        return True
    except IntegrityError as e:
        print(f'Error de clave única o clave foránea: {e}')
    except OperationalError as e:
        print(f'Error operacional\n(pérdida de conexión, falta una tabla o base de datos bloqueada): {e}')
    except DataError as e:
        print(f'Valor insertado NO corresponde: {e}')
    except PeeweeException as e:
        print(f'No se pudieron guardar los datos por un error genérico: {e}')
    return False