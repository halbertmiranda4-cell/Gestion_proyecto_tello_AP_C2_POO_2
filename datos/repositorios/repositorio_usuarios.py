from datos.modelos.models import Usuarios
from peewee import IntegrityError, OperationalError, DataError, PeeweeException


def listado_usuarios(habilitados: bool = True):
    """Por defecto lista solo los habilitados; con habilitados=False lista los eliminados."""
    usuarios = (Usuarios
                .select()
                .where(Usuarios.habilitado == int(habilitados))
                .order_by(Usuarios.id_usuario))
    if usuarios:
        return usuarios


def buscar_usuario_por_id(id_usuario: int):
    return Usuarios.get_or_none(Usuarios.id_usuario == id_usuario)


def buscar_usuario_por_correo(correo: str):
    return Usuarios.get_or_none(Usuarios.correo == correo)


def buscar_usuario_por_rut(rut: str):
    return Usuarios.get_or_none(Usuarios.rut == rut)


def guardar_usuario(usuario: Usuarios) -> bool:
    try:
        filas = usuario.save()
        if filas == 1:
            print(f'Usuario guardado con éxito con Id: {usuario.id_usuario}.')
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