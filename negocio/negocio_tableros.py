from datetime import date
from datos.modelos.models import Tablero, Lista
from datos.repositorios.repositorio_base import guardar_registro
from datos.repositorios.repositorio_proyectos import buscar_proyecto_por_id
from datos.repositorios.repositorio_tableros import (
    buscar_tablero_por_proyecto,
    listado_listas,
    siguiente_posicion_lista
)
from datos.repositorios.repositorio_tarjetas import listado_tarjetas_de_lista


def crear_tablero(id_proyecto: int, nombre: str):
    """Regla: un proyecto solo puede tener un tablero. Retorna (exito, mensaje)."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return False, 'No existe un proyecto con ese Id.'
    if buscar_tablero_por_proyecto(proyecto):
        return False, f'El proyecto "{proyecto.nompro}" ya tiene un tablero.'
    if not nombre.strip():
        return False, 'El nombre del tablero es obligatorio.'

    tablero = Tablero()
    tablero.nomtab = nombre.strip()
    tablero.id_proyecto = proyecto
    if guardar_registro(tablero):
        return True, f'Tablero "{tablero.nomtab}" creado para "{proyecto.nompro}".'
    return False, 'No se pudo crear el tablero.'


def crear_lista(id_proyecto: int, nombre: str, descripcion: str):
    """Agrega una lista al final del tablero del proyecto. Retorna (exito, mensaje)."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return False, 'No existe un proyecto con ese Id.'
    tablero = buscar_tablero_por_proyecto(proyecto)
    if not tablero:
        return False, 'El proyecto aún no tiene tablero. Créelo primero.'
    if not nombre.strip():
        return False, 'El nombre de la lista es obligatorio.'

    lista = Lista()
    lista.nomblist = nombre.strip()
    lista.descriplist = descripcion.strip() or None
    lista.id_tablero = tablero
    lista.posicion = siguiente_posicion_lista(tablero)
    if guardar_registro(lista):
        return True, f'Lista "{lista.nomblist}" creada en la posición {lista.posicion}.'
    return False, 'No se pudo crear la lista.'


def nombre_responsable(tarjeta) -> str:
    if tarjeta.id_responsable is None:
        return 'Sin asignar'
    return tarjeta.id_responsable.id_usuario.nombre


def esta_vencida(tarjeta) -> bool:
    return (tarjeta.fecha_vencimiento is not None
            and tarjeta.fecha_vencimiento < date.today()
            and tarjeta.estado != 'completada')


def obtener_tablero(id_proyecto: int):
    """Retorna (proyecto, tablero, listas). Cada lista trae sus tarjetas en lista.tarjetas.
    Si algo no existe, retorna None en esa posición."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return None, None, []
    tablero = buscar_tablero_por_proyecto(proyecto)
    if not tablero:
        return proyecto, None, []
    listas = listado_listas(tablero)
    for lista in listas:
        lista.tarjetas = listado_tarjetas_de_lista(lista)
    return proyecto, tablero, listas