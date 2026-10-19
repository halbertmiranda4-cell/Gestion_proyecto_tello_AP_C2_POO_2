from datetime import datetime


def pedir_texto(mensaje: str, obligatorio: bool = True, largo_maximo: int = None) -> str:
    """Pide un texto. Si es obligatorio, insiste hasta que no venga vacío."""
    while True:
        texto = input(mensaje).strip()
        if obligatorio and texto == '':
            print('Este dato es obligatorio.')
            continue
        if largo_maximo and len(texto) > largo_maximo:
            print(f'Máximo {largo_maximo} caracteres.')
            continue
        return texto


def pedir_entero(mensaje: str) -> int:
    """Pide un número entero sin que el programa se caiga si escriben letras."""
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print('Debe ingresar un número entero.')


def pedir_fecha(mensaje: str, obligatoria: bool = False):
    """Pide una fecha en formato dd-mm-aaaa. Retorna un date, o None si es opcional y se deja vacía."""
    while True:
        texto = input(mensaje).strip()
        if texto == '' and not obligatoria:
            return None
        try:
            return datetime.strptime(texto, '%d-%m-%Y').date()
        except ValueError:
            print('Fecha inválida. Use el formato dd-mm-aaaa (ej: 25-11-2026).')


def elegir_opcion(mensaje: str, opciones: tuple) -> str:
    """Muestra opciones numeradas y retorna la elegida. Ej: roles o estados."""
    for numero, opcion in enumerate(opciones, start=1):
        print(f'[{numero}] - {opcion}')
    while True:
        eleccion = pedir_entero(mensaje)
        if 1 <= eleccion <= len(opciones):
            return opciones[eleccion - 1]
        print(f'Elija un número entre 1 y {len(opciones)}.')