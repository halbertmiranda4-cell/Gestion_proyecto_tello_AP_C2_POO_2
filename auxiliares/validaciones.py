import re


def limpiar_rut(rut: str) -> str:
    """Quita puntos, guion y espacios. Ej: '12.345.678-5' -> '123456785'."""
    return rut.replace('.', '').replace('-', '').replace(' ', '').upper()


def calcular_dv(cuerpo: str) -> str:
    """Calcula el dígito verificador con el algoritmo módulo 11."""
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - (suma % 11)
    if resto == 11:
        return '0'
    if resto == 10:
        return 'K'
    return str(resto)


def validar_rut(rut: str) -> bool:
    rut_limpio = limpiar_rut(rut)
    if len(rut_limpio) < 2:
        return False
    cuerpo, dv = rut_limpio[:-1], rut_limpio[-1]
    if not cuerpo.isdigit():
        return False
    return calcular_dv(cuerpo) == dv


def formatear_rut(rut: str) -> str:
    """Deja el RUT siempre igual en la base de datos. Ej: '123456785' -> '12.345.678-5'."""
    rut_limpio = limpiar_rut(rut)
    cuerpo, dv = rut_limpio[:-1], rut_limpio[-1]
    cuerpo_con_puntos = f'{int(cuerpo):,}'.replace(',', '.')
    return f'{cuerpo_con_puntos}-{dv}'


def validar_correo(correo: str) -> bool:
    patron = r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$'
    return re.match(patron, correo) is not None