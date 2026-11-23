from datos.modelos.models import Etiqueta
from datos.repositorios.repositorio_etiquetas import RepositorioEtiquetas, RepositorioTarjetaEtiqueta
from datos.repositorios.repositorio_proyectos import RepositorioProyectos
from datos.repositorios.repositorio_tarjetas import RepositorioTarjetas
from negocio.servicio_base import ServicioBase
from auxiliares import colores_etiqueta


class ServicioEtiquetas(ServicioBase):
    """Reglas de negocio de las etiquetas y de su asignación a tarjetas."""

    def __init__(self):
        super().__init__(RepositorioEtiquetas())
        self.__asignaciones = RepositorioTarjetaEtiqueta()
        self.__proyectos = RepositorioProyectos()
        self.__tarjetas = RepositorioTarjetas()

    def listar(self):
        return self._repositorio.listar()

    def listar_por_proyecto(self, id_proyecto: int):
        """Retorna (proyecto, etiquetas). Si el proyecto no existe, proyecto es None."""
        proyecto = self.__proyectos.obtener_por_id(id_proyecto)
        if not proyecto:
            return None, []
        return proyecto, self._repositorio.listar_por_proyecto(proyecto)

    def crear(self, id_proyecto: int, nombre: str, color: str):
        proyecto = self.__proyectos.obtener_por_id(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'
        nombre = nombre.strip()
        if not nombre:
            return False, 'El nombre de la etiqueta es obligatorio.'
        if color not in colores_etiqueta:
            return False, 'El color no es válido.'
        if self._repositorio.buscar_por_nombre(proyecto, nombre):
            return False, f'"{proyecto}" ya tiene una etiqueta llamada "{nombre}".'

        etiqueta = Etiqueta(nometiq=nombre, color=color, id_proyecto=proyecto)
        if self._repositorio.guardar(etiqueta):
            return True, f'Etiqueta "{nombre}" ({color}) creada en "{proyecto}".'
        return False, 'No se pudo crear la etiqueta.'

    def modificar(self, id_etiqueta: int, nombre: str, color: str):
        """Vacío = no cambiar."""
        etiqueta = self.obtener(id_etiqueta)
        if not etiqueta:
            return False, 'No existe una etiqueta con ese Id.'

        cambios = []
        nombre = nombre.strip()
        if nombre and nombre != etiqueta.nometiq:
            otra = self._repositorio.buscar_por_nombre(etiqueta.id_proyecto, nombre)
            if otra and otra.id_etiqueta != etiqueta.id_etiqueta:
                return False, 'Ya existe otra etiqueta con ese nombre en el proyecto.'
            etiqueta.nometiq = nombre
            cambios.append('nombre')
        if color and color != etiqueta.color:
            if color not in colores_etiqueta:
                return False, 'El color no es válido.'
            etiqueta.color = color
            cambios.append('color')

        if not cambios:
            return False, 'No se ingresó ningún cambio.'
        if self._repositorio.guardar(etiqueta):
            return True, f'Etiqueta "{etiqueta.nometiq}" actualizada ({", ".join(cambios)}).'
        return False, 'No se pudo modificar la etiqueta.'

    def eliminar(self, id_etiqueta: int):
        """Polimorfismo: en Etiquetas, solo se elimina si ninguna tarjeta la usa."""
        etiqueta = self.obtener(id_etiqueta)
        if not etiqueta:
            return False, 'No existe una etiqueta con ese Id.'
        usos = self._repositorio.cantidad_de_usos(etiqueta)
        if usos:
            return False, (f'La etiqueta "{etiqueta.nometiq}" está en {usos} tarjeta(s). '
                           'Quítela de esas tarjetas antes de eliminarla.')
        if self._repositorio.eliminar(etiqueta):
            return True, f'Etiqueta "{etiqueta.nometiq}" eliminada.'
        return False, 'No se pudo eliminar la etiqueta.'

    def __tarjeta_y_etiqueta(self, id_tarjeta: int, id_etiqueta: int):
        """Método privado: busca ambas y revisa que sean del mismo proyecto."""
        tarjeta = self.__tarjetas.obtener_por_id(id_tarjeta)
        if not tarjeta:
            return None, None, 'No existe una tarjeta con ese Id.'
        etiqueta = self.obtener(id_etiqueta)
        if not etiqueta:
            return None, None, 'No existe una etiqueta con ese Id.'
        if etiqueta.id_proyecto.id_proyecto != tarjeta.proyecto.id_proyecto:
            return None, None, 'La etiqueta debe ser del mismo proyecto que la tarjeta.'
        return tarjeta, etiqueta, ''

    def asignar(self, id_tarjeta: int, id_etiqueta: int):
        tarjeta, etiqueta, error = self.__tarjeta_y_etiqueta(id_tarjeta, id_etiqueta)
        if error:
            return False, error
        if self.__asignaciones.buscar(tarjeta, etiqueta):
            return False, f'"{tarjeta}" ya tiene la etiqueta "{etiqueta.nometiq}".'
        if self.__asignaciones.asignar(tarjeta, etiqueta):
            return True, f'Etiqueta "{etiqueta.nometiq}" asignada a "{tarjeta}".'
        return False, 'No se pudo asignar la etiqueta.'

    def quitar(self, id_tarjeta: int, id_etiqueta: int):
        tarjeta, etiqueta, error = self.__tarjeta_y_etiqueta(id_tarjeta, id_etiqueta)
        if error:
            return False, error
        if not self.__asignaciones.buscar(tarjeta, etiqueta):
            return False, f'"{tarjeta}" no tiene la etiqueta "{etiqueta.nometiq}".'
        if self.__asignaciones.quitar(tarjeta, etiqueta):
            return True, f'Etiqueta "{etiqueta.nometiq}" quitada de "{tarjeta}".'
        return False, 'No se pudo quitar la etiqueta.'

    def etiquetas_de_tarjeta(self, tarjeta):
        return self.__asignaciones.etiquetas_de_tarjeta(tarjeta) 