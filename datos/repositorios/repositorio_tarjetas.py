from peewee import fn
from datos.modelos.models import Tablero, Lista, Tarjeta, Usuarios, UsuarioProyecto, Proyecto


def listado_tarjetas_de_lista(lista: Lista):
    return list(Tarjeta.select().where(Tarjeta.id_lista == lista).order_by(Tarjeta.posicion))


def listado_tarjetas_de_tablero(tablero: Tablero):
    return list(Tarjeta
                .select(Tarjeta)
                .join(Lista, on=(Tarjeta.id_lista == Lista.id_lista))
                .where(Lista.id_tablero == tablero))


def buscar_tarjeta_por_id(id_tarjeta: int):
    return Tarjeta.get_or_none(Tarjeta.id_tarjeta == id_tarjeta)


def siguiente_posicion_tarjeta(lista: Lista) -> int:
    maxima = Tarjeta.select(fn.MAX(Tarjeta.posicion)).where(Tarjeta.id_lista == lista).scalar()
    return (maxima or 0) + 1


def buscar_participante_por_rut(rut: str, proyecto: Proyecto):
    """Retorna el registro de usuario_proyecto si el usuario con ese RUT participa en el proyecto."""
    return (UsuarioProyecto
            .select()
            .join(Usuarios, on=(UsuarioProyecto.id_usuario == Usuarios.id_usuario))
            .where((Usuarios.rut == rut) & (UsuarioProyecto.id_proyecto == proyecto))
            .first())