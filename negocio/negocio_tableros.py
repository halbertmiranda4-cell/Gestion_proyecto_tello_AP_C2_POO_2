from datos.modelos.models import Tablero, Lista
from datos.repositorios.repositorio_proyectos import RepositorioProyectos
from datos.repositorios.repositorio_tableros import RepositorioTableros, RepositorioListas
from datos.repositorios.repositorio_tarjetas import RepositorioTarjetas
from negocio.servicio_base import ServicioBase


class ServicioTableros(ServicioBase):
    """Reglas de negocio de los tableros."""

    def __init__(self):
        super().__init__(RepositorioTableros())
        self.__proyectos = RepositorioProyectos()
        self.__listas = RepositorioListas()
        self.__tarjetas = RepositorioTarjetas()

    def listar(self):
        return self._repositorio.listar()

    def crear(self, id_proyecto: int, nombre: str):
        """Regla: un proyecto solo puede tener un tablero. Retorna (exito, mensaje)."""
        proyecto = self.__proyectos.obtener_por_id(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'
        if self._repositorio.buscar_por_proyecto(proyecto):
            return False, f'El proyecto "{proyecto}" ya tiene un tablero.'
        if not nombre.strip():
            return False, 'El nombre del tablero es obligatorio.'

        tablero = Tablero(nomtab=nombre.strip(), id_proyecto=proyecto)
        if self._repositorio.guardar(tablero):
            return True, f'Tablero "{tablero}" creado para "{proyecto}".'
        return False, 'No se pudo crear el tablero.'

    def eliminar(self, id_tablero: int):
        """Polimorfismo: en Tableros, eliminar no está permitido (el tablero vive y muere con su proyecto)."""
        return False, 'Un tablero no se elimina por separado: se elimina junto con su proyecto.'

    def obtener_tablero(self, id_proyecto: int):
        """Retorna (proyecto, tablero, listas). Cada lista trae sus tarjetas en lista.tarjetas."""
        proyecto = self.__proyectos.obtener_por_id(id_proyecto)
        if not proyecto:
            return None, None, []
        tablero = self._repositorio.buscar_por_proyecto(proyecto)
        if not tablero:
            return proyecto, None, []
        listas = self.__listas.listar_por_tablero(tablero)
        for lista in listas:
            lista.tarjetas = self.__tarjetas.listar_por_lista(lista)
        return proyecto, tablero, listas


class ServicioListas(ServicioBase):
    """Reglas de negocio de las listas."""

    def __init__(self):
        super().__init__(RepositorioListas())
        self.__proyectos = RepositorioProyectos()
        self.__tableros = RepositorioTableros()
        self.__tarjetas = RepositorioTarjetas()

    def listar(self):
        return self._repositorio.listar()

    def crear(self, id_proyecto: int, nombre: str, descripcion: str):
        """Agrega una lista al final del tablero del proyecto. Retorna (exito, mensaje)."""
        proyecto = self.__proyectos.obtener_por_id(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'
        tablero = self.__tableros.buscar_por_proyecto(proyecto)
        if not tablero:
            return False, 'El proyecto aún no tiene tablero. Créelo primero.'
        if not nombre.strip():
            return False, 'El nombre de la lista es obligatorio.'

        lista = Lista(nomblist=nombre.strip(), descriplist=descripcion.strip() or None, id_tablero=tablero,
                      posicion=self._repositorio.siguiente_posicion(tablero), habilitado=1)
        if self._repositorio.guardar(lista):
            return True, f'Lista "{lista}" creada en la posición {lista.posicion}.'
        return False, 'No se pudo crear la lista.'

    def modificar(self, id_lista: int, nombre: str, descripcion: str):
        lista = self.obtener(id_lista)
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
        if self._repositorio.guardar(lista):
            return True, f'Lista "{lista}" actualizada ({", ".join(cambios)}).'
        return False, 'No se pudo modificar la lista.'

    def eliminar(self, id_lista: int):
        """Polimorfismo: en Listas, solo se elimina si no tiene tarjetas."""
        lista = self.obtener(id_lista)
        if not lista:
            return False, 'No existe una lista con ese Id.'
        tarjetas = self.__tarjetas.listar_por_lista(lista)
        if tarjetas:
            return False, (f'La lista "{lista}" tiene {len(tarjetas)} tarjeta(s). '
                           'Muévalas o elimínelas antes de eliminar la lista.')
        if self._repositorio.eliminar(lista):
            return True, f'Lista "{lista}" eliminada.'
        return False, 'No se pudo eliminar la lista.' 