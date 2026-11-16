from peewee import fn
from datos.modelos.models import Proyecto, Tablero, Lista
from datos.repositorios.repositorio_base import RepositorioBase, RepositorioBorradoLogico


class RepositorioTableros(RepositorioBase):
    """Acceso a datos de Tablero."""

    def __init__(self):
        super().__init__(Tablero)

    def buscar_por_proyecto(self, proyecto: Proyecto):
        return Tablero.get_or_none(Tablero.id_proyecto == proyecto)


class RepositorioListas(RepositorioBorradoLogico):
    """Acceso a datos de Lista (con borrado lógico)."""

    def __init__(self):
        super().__init__(Lista)

    def listar_por_tablero(self, tablero: Tablero):
        return list(self._consulta_base().where(Lista.id_tablero == tablero).order_by(Lista.posicion))

    def siguiente_posicion(self, tablero: Tablero) -> int:
        maxima = Lista.select(fn.MAX(Lista.posicion)).where(Lista.id_tablero == tablero).scalar()
        return (maxima or 0) + 1 