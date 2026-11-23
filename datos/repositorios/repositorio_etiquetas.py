from peewee import PeeweeException
from datos.modelos.models import Etiqueta, TarjetaEtiqueta, Proyecto, Tarjeta
from datos.repositorios.repositorio_base import RepositorioBase


class RepositorioEtiquetas(RepositorioBase):
    """Acceso a datos de Etiqueta."""

    def __init__(self):
        super().__init__(Etiqueta)

    def listar_por_proyecto(self, proyecto: Proyecto):
        return list(Etiqueta.select().where(Etiqueta.id_proyecto == proyecto).order_by(Etiqueta.nometiq))

    def buscar_por_nombre(self, proyecto: Proyecto, nombre: str):
        return Etiqueta.get_or_none((Etiqueta.id_proyecto == proyecto) & (Etiqueta.nometiq == nombre))

    def cantidad_de_usos(self, etiqueta: Etiqueta) -> int:
        return TarjetaEtiqueta.select().where(TarjetaEtiqueta.id_etiqueta == etiqueta).count()

    def eliminar(self, etiqueta: Etiqueta) -> bool:
        return etiqueta.delete_instance() == 1


class RepositorioTarjetaEtiqueta(RepositorioBase):
    """Acceso a datos de TarjetaEtiqueta (qué etiquetas tiene cada tarjeta)."""

    def __init__(self):
        super().__init__(TarjetaEtiqueta)

    def buscar(self, tarjeta: Tarjeta, etiqueta: Etiqueta):
        return TarjetaEtiqueta.get_or_none(
            (TarjetaEtiqueta.id_tarjeta == tarjeta) & (TarjetaEtiqueta.id_etiqueta == etiqueta))

    def etiquetas_de_tarjeta(self, tarjeta: Tarjeta):
        return list(Etiqueta
                    .select()
                    .join(TarjetaEtiqueta, on=(TarjetaEtiqueta.id_etiqueta == Etiqueta.id_etiqueta))
                    .where(TarjetaEtiqueta.id_tarjeta == tarjeta)
                    .order_by(Etiqueta.nometiq))

    def asignar(self, tarjeta: Tarjeta, etiqueta: Etiqueta) -> bool:
        # La clave primaria es compuesta (tarjeta, etiqueta): se inserta con create()
        try:
            TarjetaEtiqueta.create(id_tarjeta=tarjeta, id_etiqueta=etiqueta)
            return True
        except PeeweeException as e:
            print(f'No se pudo asignar la etiqueta: {e}')
            return False

    def quitar(self, tarjeta: Tarjeta, etiqueta: Etiqueta) -> bool:
        borradas = (TarjetaEtiqueta.delete()
                    .where((TarjetaEtiqueta.id_tarjeta == tarjeta) & (TarjetaEtiqueta.id_etiqueta == etiqueta))
                    .execute())
        return borradas == 1 