from datetime import date
from datos.modelos.models import Tablero, Lista
from datos.repositorios.repositorio_base import guardar_registro
from datos.repositorios.repositorio_proyectos import buscar_proyecto_por_id
from datos.repositorios.repositorio_tableros import (
    buscar_tablero_por_proyecto,
    listado_listas,
    buscar_lista_por_id,
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
    lista.habilitado = 1
    if guardar_registro(lista):
        return True, f'Lista "{lista.nomblist}" creada en la posición {lista.posicion}.'
    return False, 'No se pudo crear la lista.'


def obtener_lista(id_lista: int):
    return buscar_lista_por_id(id_lista)


def modificar_lista(id_lista: int, nombre: str, descripcion: str):
    """Modifica nombre y/o descripción. Un campo vacío significa "no cambiar".
    Retorna (exito, mensaje)."""
    lista = buscar_lista_por_id(id_lista)
    if not lista:
        return False, 'No existe una lista con ese Id.'

    cambios = []
    nombre = nombre.strip()
    if nombre and nombre != lista.nomblist:
        lista.nomblist = nombre
        cambios.append('nombre')
    descripcion = descripcion.strip()
    if descripcion and descripcion != lista.descriplist:
        lista.descriplist = descripcion
        cambios.append('descripción')

    if not cambios:
        return False, 'No se ingresó ningún cambio.'
    if guardar_registro(lista):
        return True, f'Lista "{lista.nomblist}" actualizada ({", ".join(cambios)}).'
    return False, 'No se pudo modificar la lista.'


def eliminar_lista(id_lista: int):
    """Borrado lógico. Regla: no se puede eliminar una lista que todavía tiene tarjetas
    (hay que moverlas o eliminarlas primero). Retorna (exito, mensaje)."""
    lista = buscar_lista_por_id(id_lista)
    if not lista:
        return False, 'No existe una lista con ese Id.'
    tarjetas = listado_tarjetas_de_lista(lista)
    if tarjetas:
        return False, (f'La lista "{lista.nomblist}" tiene {len(tarjetas)} tarjeta(s). '
                       'Muévalas o elimínelas antes de eliminar la lista.')

    lista.habilitado = 0
    if guardar_registro(lista):
        return True, f'Lista "{lista.nomblist}" eliminada.'
    return False, 'No se pudo eliminar la lista.'


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