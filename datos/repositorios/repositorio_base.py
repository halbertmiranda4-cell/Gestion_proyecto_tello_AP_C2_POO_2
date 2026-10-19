from peewee import IntegrityError, OperationalError, DataError, PeeweeException


def guardar_registro(registro) -> bool:
    """Guarda (inserta o actualiza) cualquier modelo de Peewee manejando los errores.
    Se usa para no repetir el mismo try/except en cada repositorio."""
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