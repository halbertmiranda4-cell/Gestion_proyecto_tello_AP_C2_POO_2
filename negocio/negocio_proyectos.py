from datos.modelos.models import Proyecto, UsuarioProyecto
from datos.repositorios.repositorio_proyectos import RepositorioProyectos, RepositorioParticipantes
from datos.repositorios.repositorio_usuarios import RepositorioUsuarios
from negocio.servicio_base import ServicioBase
from auxiliares import Rut, roles_proyecto


class ServicioProyectos(ServicioBase):
    """Reglas de negocio de los proyectos y sus participantes."""

    def __init__(self):
        super().__init__(RepositorioProyectos())
        self.__participantes = RepositorioParticipantes()   # privado
        self.__usuarios = RepositorioUsuarios()             # privado

    def listar(self):
        return self._repositorio.listar_con_participantes()

    def __buscar_usuario(self, rut: str):
        rut = Rut(rut)
        if not rut.es_valido():
            return None
        return self.__usuarios.buscar_por_rut(rut.formateado())

    def crear(self, nombre: str, descripcion: str, rut_creador: str):
        """Crea el proyecto y deja a quien lo crea como administrador. Retorna (exito, mensaje)."""
        nombre = nombre.strip()
        if not nombre:
            return False, 'El nombre del proyecto es obligatorio.'
        if self._repositorio.buscar_por_nombre(nombre):
            return False, 'Ya existe un proyecto con ese nombre.'
        creador = self.__buscar_usuario(rut_creador)
        if not creador:
            return False, 'No existe un usuario con ese RUT.'
        if not creador.esta_habilitado:
            return False, f'{creador.nombre} está deshabilitado y no puede crear proyectos.'

        proyecto = Proyecto(nompro=nombre, descripcion=descripcion.strip() or None, habilitado=1)
        if self._repositorio.guardar_con_administrador(proyecto, creador):
            return True, f'Proyecto "{proyecto}" creado (Id {proyecto.id_proyecto}). {creador.nombre} quedó como administrador.'
        return False, 'No se pudo crear el proyecto.'

    def modificar(self, id_proyecto: int, nombre: str, descripcion: str):
        """Modifica nombre y/o descripción. Vacío = no cambiar. Retorna (exito, mensaje)."""
        proyecto = self.obtener(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'

        cambios = []
        nombre = nombre.strip()
        if nombre and nombre != proyecto.nompro:
            otro = self._repositorio.buscar_por_nombre(nombre)
            if otro and otro.id_proyecto != proyecto.id_proyecto:
                return False, 'Ya existe otro proyecto con ese nombre.'
            proyecto.nompro = nombre
            cambios.append('nombre')
        descripcion = descripcion.strip()
        if descripcion and descripcion != proyecto.descripcion:
            proyecto.descripcion = descripcion
            cambios.append('descripción')

        if not cambios:
            return False, 'No se ingresó ningún cambio.'
        if self._repositorio.guardar(proyecto):
            return True, f'Proyecto "{proyecto}" actualizado ({", ".join(cambios)}).'
        return False, 'No se pudo modificar el proyecto.'

    def eliminar(self, id_proyecto: int):
        """Polimorfismo: en Proyectos, eliminar = borrado lógico del proyecto."""
        proyecto = self.obtener(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'
        if self._repositorio.eliminar(proyecto):
            return True, f'Proyecto "{proyecto}" eliminado.'
        return False, 'No se pudo eliminar el proyecto.'

    def __buscar_participante(self, proyecto, rut: str):
        rut = Rut(rut)
        if not rut.es_valido():
            return None
        return self.__participantes.buscar_por_rut(rut.formateado(), proyecto)

    def verificar_permiso_eliminar(self, id_proyecto: int, rut_solicitante: str):
        """Polimorfismo: es el ROL (Administrador o Miembro) el que responde si puede eliminar."""
        proyecto = self.obtener(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'
        solicitante = self.__buscar_participante(proyecto, rut_solicitante)
        if not solicitante:
            return False, f'Ese usuario no participa en el proyecto "{proyecto}".'
        if not solicitante.rol_actual.puede_eliminar_proyecto():
            return False, f'Un {solicitante.rol_actual} no puede eliminar el proyecto.'
        return True, ''

    def agregar_participante(self, id_proyecto: int, rut_solicitante: str, rut: str, rol: str):
        proyecto = self.obtener(id_proyecto)
        if not proyecto:
            return False, 'No existe un proyecto con ese Id.'
        solicitante = self.__buscar_participante(proyecto, rut_solicitante)
        if not solicitante:
            return False, f'Quien agrega debe participar en el proyecto "{proyecto}".'
        # Polimorfismo: Administrador responde True, Miembro responde False
        if not solicitante.rol_actual.puede_gestionar_participantes():
            return False, f'Un {solicitante.rol_actual} no puede agregar participantes.'
        usuario = self.__buscar_usuario(rut)
        if not usuario:
            return False, 'No existe un usuario con ese RUT.'
        if not usuario.esta_habilitado:
            return False, f'{usuario.nombre} está deshabilitado y no puede unirse a proyectos.'
        if rol not in roles_proyecto:
            return False, 'El rol no es válido.'
        if self.__participantes.buscar(usuario, proyecto):
            return False, f'{usuario.nombre} ya participa en este proyecto.'

        participante = UsuarioProyecto(id_usuario=usuario, id_proyecto=proyecto, rol=rol)
        if self.__participantes.guardar(participante):
            return True, f'{usuario.nombre} agregado a "{proyecto}" como {rol}.'
        return False, 'No se pudo agregar el participante.'

    def listar_participantes(self, id_proyecto: int):
        """Retorna (proyecto, participantes). Si el proyecto no existe, proyecto es None."""
        proyecto = self.obtener(id_proyecto)
        if not proyecto:
            return None, []
        return proyecto, self.__participantes.listar_por_proyecto(proyecto) 