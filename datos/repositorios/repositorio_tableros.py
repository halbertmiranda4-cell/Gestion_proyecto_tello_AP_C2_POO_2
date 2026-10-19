from peewee import fn
from datos.modelos.models import Proyecto, Tablero, Lista


def buscar_tablero_por_proyecto(proyecto: Proyecto):
    return Tablero.get_or_none(Tablero.id_proyecto == proyecto)


def listado_listas(tablero: Tablero):
    return list(Lista.select().where(Lista.id_tablero == tablero).order_by(Lista.posicion))


def buscar_lista_por_id(id_lista: int):
    return Lista.get_or_none(Lista.id_lista == id_lista)


def siguiente_posicion_lista(tablero: Tablero) -> int:
    maxima = Lista.select(fn.MAX(Lista.posicion)).where(Lista.id_tablero == tablero).scalar()
    return (maxima or 0) + 1