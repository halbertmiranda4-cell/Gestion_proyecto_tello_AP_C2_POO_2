from peewee import IntegrityError, OperationalError, DataError, PeeweeException


class RepositorioBase:
    """Clase padre de todos los repositorios (herencia).
    Tiene el acceso a datos que es igual para todas las entidades, así no se repite código."""

    def __init__(self, modelo):
        self._modelo = modelo   # atributo protegido: lo usan solo esta clase y sus hijas

    def _consulta_base(self):
        """Consulta de partida. Las clases hijas la pueden redefinir (polimorfismo)."""
        return self._modelo.select()

    def obtener_por_id(self, id_registro):
        clave = self._modelo._meta.primary_key
        return self._consulta_base().where(clave == id_registro).first()

    def listar(self):
        return list(self._consulta_base().order_by(self._modelo._meta.primary_key))

    def guardar(self, registro) -> bool:
        """Inserta o actualiza cualquier modelo manejando los errores de Peewee."""
        try:
            registro.save()
            return True
        except IntegrityError as e:
            print(f'Error de clave única o clave foránea: {e}')
        except OperationalError as e:
            print(f'Error operacional\n(pérdida de conexión, falta una tabla o base de datos bloqueada): {e}')
        except DataError as e:
            print(f'Valor insertado NO corresponde: {e}')
        except PeeweeException as e:
            print(f'No se pudieron guardar los datos por un error genérico: {e}')
        return False


class RepositorioBorradoLogico(RepositorioBase):
    """Repositorio para entidades con borrado lógico (Proyecto, Lista, Tarjeta).

    Polimorfismo: redefine _consulta_base() para ignorar los registros eliminados.
    Por eso obtener_por_id() y listar(), heredados del padre, solo devuelven registros habilitados."""

    def _consulta_base(self):
        return self._modelo.select().where(self._modelo.habilitado == 1)

    def eliminar(self, registro) -> bool:
        registro.deshabilitar()
        return self.guardar(registro) 