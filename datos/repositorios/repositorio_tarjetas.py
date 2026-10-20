from peewee import fn
from datos.modelos.models import Tablero, Lista, Tarjeta, Usuarios, UsuarioProyecto, Proyecto


def listado_tarjetas_de_lista(lista: Lista):
    # Solo tarjetas habilitadas, ordenadas por posición
    return list(Tarjeta
                .select()
                .where((Tarjeta.id_lista == lista) & (Tarjeta.habilitado == 1))
                .order_by(Tarjeta.posicion))


def listado_tarjetas_de_tablero(tablero: Tablero):
    # Tarjetas habilitadas que están en listas habilitadas del tablero (se usa en el reporte)
    return list(Tarjeta
                .select(Tarjeta)
                .join(Lista, on=(Tarjeta.id_lista == Lista.id_lista))
                .where((Lista.id_tablero == tablero) & (Lista.habilitado == 1) & (Tarjeta.habilitado == 1)))


def buscar_tarjeta_por_id(id_tarjeta: int):
    return Tarjeta.get_or_none((Tarjeta.id_tarjeta == id_tarjeta) & (Tarjeta.habilitado == 1))


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