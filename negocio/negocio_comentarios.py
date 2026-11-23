from datos.modelos.models import Comentario
from datos.repositorios.repositorio_comentarios import RepositorioComentarios
from datos.repositorios.repositorio_tarjetas import RepositorioTarjetas
from negocio.servicio_base import ServicioBase


class ServicioComentarios(ServicioBase):
    """Reglas de negocio de los comentarios de una tarjeta."""

    LARGO_MAXIMO = 500

    def __init__(self):
        super().__init__(RepositorioComentarios())
        self.__tarjetas = RepositorioTarjetas()

    def listar(self):
        return self._repositorio.listar()

    def crear(self, id_tarjeta: int, autor, texto: str):
        """autor: el usuario que inició sesión. Retorna (exito, mensaje)."""
        tarjeta = self.__tarjetas.obtener_por_id(id_tarjeta)
        if not tarjeta:
            return False, 'No existe una tarjeta con ese Id.'
        texto = texto.strip()
        if not texto:
            return False, 'El comentario no puede estar vacío.'
        if len(texto) > self.LARGO_MAXIMO:
            return False, f'El comentario puede tener como máximo {self.LARGO_MAXIMO} caracteres.'

        comentario = Comentario(texto=texto, id_usuario=autor, id_tarjeta=tarjeta)
        if self._repositorio.guardar(comentario):
            return True, f'Comentario agregado a "{tarjeta}".'
        return False, 'No se pudo guardar el comentario.'

    def listar_por_tarjeta(self, id_tarjeta: int):
        """Retorna (tarjeta, comentarios). Si la tarjeta no existe, tarjeta es None."""
        tarjeta = self.__tarjetas.obtener_por_id(id_tarjeta)
        if not tarjeta:
            return None, []
        return tarjeta, self._repositorio.listar_por_tarjeta(tarjeta)

    def verificar_autor(self, id_comentario: int, usuario):
        """Regla: solo quien escribió el comentario puede eliminarlo."""
        comentario = self.obtener(id_comentario)
        if not comentario:
            return False, 'No existe un comentario con ese Id.'
        if comentario.id_usuario.id_usuario != usuario.id_usuario:
            return False, 'Solo el autor del comentario puede eliminarlo.'
        return True, ''

    def eliminar(self, id_comentario: int):
        """Polimorfismo: en Comentarios, eliminar = borrado físico (no tiene campo habilitado)."""
        comentario = self.obtener(id_comentario)
        if not comentario:
            return False, 'No existe un comentario con ese Id.'
        if self._repositorio.eliminar(comentario):
            return True, 'Comentario eliminado.'
        return False, 'No se pudo eliminar el comentario.' 