from datos.repositorios.repositorio_proyectos import RepositorioProyectos
from datos.repositorios.repositorio_tableros import RepositorioTableros
from datos.repositorios.repositorio_tarjetas import RepositorioTarjetas
from auxiliares import estados_tarjeta


class ServicioReporte:
    """Calcula el avance de un proyecto. No hereda de ServicioBase porque no es un CRUD."""

    def __init__(self):
        self.__proyectos = RepositorioProyectos()
        self.__tableros = RepositorioTableros()
        self.__tarjetas = RepositorioTarjetas()

    def reporte_avance(self, id_proyecto: int):
        """Retorna (exito, mensaje, datos)."""
        proyecto = self.__proyectos.obtener_por_id(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.', None
        tablero = self.__tableros.buscar_por_proyecto(proyecto)
        if not tablero:
            return False, f'"{proyecto}" aún no tiene tablero.', None

        tarjetas = self.__tarjetas.listar_por_tablero(tablero)
        por_estado = {estado: 0 for estado in estados_tarjeta}
        por_responsable = {}
        vencidas = []
        avance = 0.0

        for tarjeta in tarjetas:
            por_estado[tarjeta.estado] = por_estado.get(tarjeta.estado, 0) + 1
            responsable = tarjeta.nombre_responsable
            conteo = por_responsable.setdefault(responsable, {'total': 0, 'completadas': 0})
            conteo['total'] += 1
            if tarjeta.estado == 'completada':
                conteo['completadas'] += 1
            # Polimorfismo: cada estado sabe cuánto aporta (pendiente 0, en progreso 0.5, completada 1)
            avance += tarjeta.estado_actual.aporte_avance()
            if tarjeta.esta_vencida():
                vencidas.append(tarjeta)

        total = len(tarjetas)
        completadas = por_estado.get('completada', 0)
        datos = {
            'proyecto': proyecto,
            'total': total,
            'completadas': completadas,
            'porcentaje': round(completadas * 100 / total) if total else 0,
            'avance_ponderado': round(avance * 100 / total) if total else 0,
            'por_estado': por_estado,
            'por_responsable': por_responsable,
            'vencidas': vencidas
        }
        return True, '', datos 