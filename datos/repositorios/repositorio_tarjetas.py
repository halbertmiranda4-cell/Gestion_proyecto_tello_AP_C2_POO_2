from peewee import fn
from datos.modelos.models import Tablero, Lista, Tarjeta
from datos.repositorios.repositorio_base import RepositorioBorradoLogico


class RepositorioTarjetas(RepositorioBorradoLogico):
    """Acceso a datos de Tarjeta (con borrado lógico)."""

    def __init__(self):
        super().__init__(Tarjeta)

    def listar_por_lista(self, lista: Lista):
        return list(self._consulta_base().where(Tarjeta.id_lista == lista).order_by(Tarjeta.posicion))

    def listar_por_tablero(self, tablero: Tablero):
        # Tarjetas habilitadas que están en listas habilitadas del tablero (se usa en el reporte)
        return list(self._consulta_base()
                    .join(Lista, on=(Tarjeta.id_lista == Lista.id_lista))
                    .where((Lista.id_tablero == tablero) & (Lista.habilitado == 1)))

    def siguiente_posicion(self, lista: Lista) -> int:
        maxima = Tarjeta.select(fn.MAX(Tarjeta.posicion)).where(Tarjeta.id_lista == lista).scalar()
        return (maxima or 0) + 1 