from datetime import date
from datos.modelos.models import Tarjeta
from datos.repositorios.repositorio_tarjetas import RepositorioTarjetas
from datos.repositorios.repositorio_tableros import RepositorioListas
from datos.repositorios.repositorio_proyectos import RepositorioParticipantes
from negocio.servicio_base import ServicioBase
from auxiliares import Rut, estados_tarjeta


class ServicioTarjetas(ServicioBase):
    """Reglas de negocio de las tarjetas."""

    def __init__(self):
        super().__init__(RepositorioTarjetas())
        self.__listas = RepositorioListas()
        self.__participantes = RepositorioParticipantes()

    def listar(self):
        return self._repositorio.listar()

    def crear(self, id_lista: int, nombre: str, descripcion: str, fecha_vencimiento):
        """Crea una tarjeta al final de la lista. fecha_vencimiento: date o None. Retorna (exito, mensaje)."""
        lista = self.__listas.obtener_por_id(id_lista)
        if not lista:
            return False, 'No existe una lista con ese Id.'
        if not nombre.strip():
            return False, 'El nombre de la tarjeta es obligatorio.'
        if fecha_vencimiento and fecha_vencimiento < date.today():
            return False, 'La fecha límite no puede ser anterior a hoy.'

        tarjeta = Tarjeta(nombtarj=nombre.strip(), descriptarj=descripcion.strip() or None,
                          fecha_vencimiento=fecha_vencimiento, estado='pendiente', id_lista=lista,
                          posicion=self._repositorio.siguiente_posicion(lista), habilitado=1)
        if self._repositorio.guardar(tarjeta):
            return True, f'Tarjeta "{tarjeta}" creada en "{lista}" (Id {tarjeta.id_tarjeta}).'
        return False, 'No se pudo crear la tarjeta.'

    def modificar(self, id_tarjeta: int, nombre: str, descripcion: str, fecha_vencimiento):
        """Vacío o None = no cambiar. Regla: la fecha límite no puede ser anterior a la creación."""
        tarjeta = self.obtener(id_tarjeta)
        if not tarjeta:
            return False, 'No existe una tarjeta con ese Id.'

        cambios = []
        nombre = nombre.strip()
        if nombre and nombre != tarjeta.nombtarj:
            tarjeta.nombtarj = nombre
            cambios.append('nombre')
        descripcion = descripcion.strip()
        if descripcion and descripcion != tarjeta.descriptarj:
            tarjeta.descriptarj = descripcion
            cambios.append('descripción')
        if fecha_vencimiento and fecha_vencimiento != tarjeta.fecha_vencimiento:
            if tarjeta.fecha_creacion and fecha_vencimiento < tarjeta.fecha_creacion:
                return False, 'La fecha límite no puede ser anterior a la fecha de creación de la tarjeta.'
            tarjeta.fecha_vencimiento = fecha_vencimiento
            cambios.append('fecha límite')

        if not cambios:
            return False, 'No se ingresó ningún cambio.'
        if self._repositorio.guardar(tarjeta):
            return True, f'Tarjeta "{tarjeta}" actualizada ({", ".join(cambios)}).'
        return False, 'No se pudo modificar la tarjeta.'

    def eliminar(self, id_tarjeta: int):
        """Polimorfismo: en Tarjetas, eliminar = borrado lógico (deja de verse y de contar en el reporte)."""
        tarjeta = self.obtener(id_tarjeta)
        if not tarjeta:
            return False, 'No existe una tarjeta con ese Id.'
        if self._repositorio.eliminar(tarjeta):
            return True, f'Tarjeta "{tarjeta}" eliminada.'
        return False, 'No se pudo eliminar la tarjeta.'

    def mover(self, id_tarjeta: int, id_lista_destino: int):
        """Regla: solo se mueve entre listas del MISMO tablero."""
        tarjeta = self.obtener(id_tarjeta)
        if not tarjeta:
            return False, 'No existe una tarjeta con ese Id.'
        destino = self.__listas.obtener_por_id(id_lista_destino)
        if not destino:
            return False, 'No existe una lista con ese Id.'
        origen = tarjeta.id_lista
        if destino.id_lista == origen.id_lista:
            return False, 'La tarjeta ya está en esa lista.'
        if destino.id_tablero.id_tablero != origen.id_tablero.id_tablero:
            return False, 'Solo se puede mover a una lista del mismo tablero.'

        tarjeta.id_lista = destino
        tarjeta.posicion = self._repositorio.siguiente_posicion(destino)
        if self._repositorio.guardar(tarjeta):
            return True, f'"{tarjeta}" movida de "{origen}" a "{destino}".'
        return False, 'No se pudo mover la tarjeta.'

    def asignar_responsable(self, id_tarjeta: int, rut: str):
        """Regla: el responsable debe ser participante habilitado del proyecto."""
        tarjeta = self.obtener(id_tarjeta)
        if not tarjeta:
            return False, 'No existe una tarjeta con ese Id.'
        rut = Rut(rut)
        if not rut.es_valido():
            return False, 'El RUT no es válido.'
        participante = self.__participantes.buscar_por_rut(rut.formateado(), tarjeta.proyecto)
        if not participante:
            return False, f'Ese usuario no participa en el proyecto "{tarjeta.proyecto}".'
        if not participante.id_usuario.esta_habilitado:
            return False, f'{participante.id_usuario.nombre} está deshabilitado y no puede recibir tarjetas.'

        tarjeta.id_responsable = participante
        if self._repositorio.guardar(tarjeta):
            return True, f'{participante.id_usuario.nombre} es ahora responsable de "{tarjeta}".'
        return False, 'No se pudo asignar el responsable.'

    def cambiar_estado(self, id_tarjeta: int, estado: str):
        """Regla: solo se aceptan los estados definidos en la aplicación."""
        tarjeta = self.obtener(id_tarjeta)
        if not tarjeta:
            return False, 'No existe una tarjeta con ese Id.'
        if estado not in estados_tarjeta:
            return False, 'El estado no es válido.'
        if tarjeta.estado == estado:
            return False, f'La tarjeta ya está "{estado}".'

        tarjeta.estado = estado
        if self._repositorio.guardar(tarjeta):
            return True, f'"{tarjeta}" ahora está "{estado}".'
        return False, 'No se pudo cambiar el estado.' 