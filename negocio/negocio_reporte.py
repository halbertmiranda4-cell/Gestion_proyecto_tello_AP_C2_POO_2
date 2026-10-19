from datos.repositorios.repositorio_proyectos import buscar_proyecto_por_id
from datos.repositorios.repositorio_tableros import buscar_tablero_por_proyecto
from datos.repositorios.repositorio_tarjetas import listado_tarjetas_de_tablero
from negocio.negocio_tableros import nombre_responsable, esta_vencida
from auxiliares import estados_tarjeta


def reporte_avance(id_proyecto: int):
    """Calcula el avance de un proyecto. Retorna (exito, mensaje, datos)."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return False, 'No existe un proyecto con ese Id.', None
    tablero = buscar_tablero_por_proyecto(proyecto)
    if not tablero:
        return False, f'"{proyecto.nompro}" aún no tiene tablero.', None

    tarjetas = listado_tarjetas_de_tablero(tablero)
    total = len(tarjetas)

    por_estado = {estado: 0 for estado in estados_tarjeta}
    por_responsable = {}
    vencidas = []

    for tarjeta in tarjetas:
        por_estado[tarjeta.estado] = por_estado.get(tarjeta.estado, 0) + 1

        responsable = nombre_responsable(tarjeta)
        if responsable not in por_responsable:
            por_responsable[responsable] = {'total': 0, 'completadas': 0}
        por_responsable[responsable]['total'] += 1
        if tarjeta.estado == 'completada':
            por_responsable[responsable]['completadas'] += 1

        if esta_vencida(tarjeta):
            vencidas.append(tarjeta)

    completadas = por_estado.get('completada', 0)
    porcentaje = round(completadas * 100 / total) if total else 0

    datos = {
        'proyecto': proyecto,
        'total': total,
        'completadas': completadas,
        'porcentaje': porcentaje,
        'por_estado': por_estado,
        'por_responsable': por_responsable,
        'vencidas': vencidas
    }
    return True, '', datos