from datos.modelos.models import Comentario, Usuarios, Tarjeta
from datos.repositorios.repositorio_base import RepositorioBase


class RepositorioComentarios(RepositorioBase):
    """Acceso a datos de Comentario. Hereda guardar, obtener_por_id y listar de RepositorioBase."""

    def __init__(self):
        super().__init__(Comentario)

    def listar_por_tarjeta(self, tarjeta: Tarjeta):
        return list(Comentario
                    .select(Comentario, Usuarios)
                    .join(Usuarios, on=(Comentario.id_usuario == Usuarios.id_usuario))
                    .where(Comentario.id_tarjeta == tarjeta)
                    .order_by(Comentario.fecha_creacion, Comentario.id_comentario))

    def eliminar(self, comentario: Comentario) -> bool:
        """Un comentario no tiene campo habilitado: se borra de verdad (borrado físico)."""
        return comentario.delete_instance() == 1 