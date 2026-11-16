from peewee import fn, JOIN, PeeweeException
from datos.modelos.models import database, Proyecto, UsuarioProyecto, Usuarios
from datos.repositorios.repositorio_base import RepositorioBase, RepositorioBorradoLogico


class RepositorioProyectos(RepositorioBorradoLogico):
    """Acceso a datos de Proyecto (con borrado lógico)."""

    def __init__(self):
        super().__init__(Proyecto)

    def listar_con_participantes(self):
        # Cada proyecto con la cantidad de participantes (LEFT JOIN para incluir proyectos sin participantes)
        return list(Proyecto
                    .select(Proyecto, fn.COUNT(UsuarioProyecto.id_usuario_proyecto).alias('participantes'))
                    .join(UsuarioProyecto, JOIN.LEFT_OUTER, on=(UsuarioProyecto.id_proyecto == Proyecto.id_proyecto))
                    .where(Proyecto.habilitado == 1)
                    .group_by(Proyecto.id_proyecto)
                    .order_by(Proyecto.id_proyecto))

    def buscar_por_nombre(self, nombre: str):
        return self._consulta_base().where(Proyecto.nompro == nombre).first()

    def guardar_con_administrador(self, proyecto: Proyecto, usuario: Usuarios) -> bool:
        # atomic(): se guardan el proyecto y su administrador juntos, o no se guarda nada
        try:
            with database.atomic():
                proyecto.save()
                UsuarioProyecto.create(id_usuario=usuario, id_proyecto=proyecto, rol='administrador')
            return True
        except PeeweeException as e:
            print(f'No se pudo guardar el proyecto: {e}')
            return False


class RepositorioParticipantes(RepositorioBase):
    """Acceso a datos de UsuarioProyecto (participación de un usuario en un proyecto)."""

    def __init__(self):
        super().__init__(UsuarioProyecto)

    def buscar(self, usuario: Usuarios, proyecto: Proyecto):
        return UsuarioProyecto.get_or_none(
            (UsuarioProyecto.id_usuario == usuario) & (UsuarioProyecto.id_proyecto == proyecto))

    def buscar_por_rut(self, rut: str, proyecto: Proyecto):
        return (UsuarioProyecto
                .select()
                .join(Usuarios, on=(UsuarioProyecto.id_usuario == Usuarios.id_usuario))
                .where((Usuarios.rut == rut) & (UsuarioProyecto.id_proyecto == proyecto))
                .first())

    def listar_por_proyecto(self, proyecto: Proyecto):
        return list(UsuarioProyecto
                    .select(UsuarioProyecto, Usuarios)
                    .join(Usuarios, on=(UsuarioProyecto.id_usuario == Usuarios.id_usuario))
                    .where(UsuarioProyecto.id_proyecto == proyecto)
                    .order_by(UsuarioProyecto.rol, Usuarios.nombre)) 