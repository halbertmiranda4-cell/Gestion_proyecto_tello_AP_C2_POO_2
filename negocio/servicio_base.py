from abc import ABC, abstractmethod


class ServicioBase(ABC):
    """Clase abstracta de la capa de negocio.

    Abstracción: define QUÉ debe saber hacer todo servicio (listar y eliminar) sin decir CÓMO.
    No se puede instanciar directamente: cada entidad tiene su propia clase hija que implementa
    esos métodos con sus reglas (polimorfismo).
    """

    def __init__(self, repositorio):
        self._repositorio = repositorio   # protegido: la presentación nunca accede a la base de datos

    def obtener(self, id_registro):
        """Común para todos los servicios (se hereda tal cual)."""
        return self._repositorio.obtener_por_id(id_registro)

    @abstractmethod
    def listar(self):
        """Retorna la lista de registros que se pueden mostrar."""

    @abstractmethod
    def eliminar(self, id_registro: int):
        """Elimina un registro aplicando las reglas de cada entidad. Retorna (exito, mensaje).""" 