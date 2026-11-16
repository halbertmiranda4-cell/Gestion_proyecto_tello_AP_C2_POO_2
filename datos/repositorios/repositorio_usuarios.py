from datos.modelos.models import Usuarios
from datos.repositorios.repositorio_base import RepositorioBase


class RepositorioUsuarios(RepositorioBase):
    """Acceso a datos de Usuarios. Hereda guardar, obtener_por_id y listar de RepositorioBase.
    No usa RepositorioBorradoLogico porque un usuario deshabilitado se debe poder encontrar
    para volver a habilitarlo."""

    def __init__(self):
        super().__init__(Usuarios)

    def listar_por_estado(self, habilitados: bool = True):
        return list(Usuarios
                    .select()
                    .where(Usuarios.habilitado == int(habilitados))
                    .order_by(Usuarios.id_usuario))

    def buscar_por_correo(self, correo: str):
        return Usuarios.get_or_none(Usuarios.correo == correo)

    def buscar_por_rut(self, rut: str):
        return Usuarios.get_or_none(Usuarios.rut == rut) 