import re


class Rut:
    """Representa un RUT chileno.

    Encapsulamiento: el cuerpo y el dígito verificador son atributos privados (__cuerpo, __dv).
    Desde afuera solo se puede consultar si es válido o pedirlo formateado, nunca modificarlos.
    """

    def __init__(self, texto: str):
        limpio = str(texto).replace('.', '').replace('-', '').replace(' ', '').upper()
        self.__cuerpo = limpio[:-1]
        self.__dv = limpio[-1:] if limpio else ''

    @property
    def cuerpo(self) -> str:
        return self.__cuerpo

    @property
    def digito_verificador(self) -> str:
        return self.__dv

    @staticmethod
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

    def es_valido(self) -> bool:
        if not self.__cuerpo.isdigit() or not self.__dv:
            return False
        return Rut.calcular_dv(self.__cuerpo) == self.__dv

    def formateado(self) -> str:
        """Ej: '123456785' -> '12.345.678-5'. Así el RUT se guarda siempre igual en la base de datos."""
        cuerpo_con_puntos = f'{int(self.__cuerpo):,}'.replace(',', '.')
        return f'{cuerpo_con_puntos}-{self.__dv}'

    def __str__(self) -> str:
        return self.formateado() if self.es_valido() else f'{self.__cuerpo}-{self.__dv}'


# Funciones de apoyo (atajos para no crear el objeto cada vez)
def validar_rut(rut: str) -> bool:
    return Rut(rut).es_valido()


def formatear_rut(rut: str) -> str:
    return Rut(rut).formateado()


def validar_correo(correo: str) -> bool:
    patron = r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$'
    return re.match(patron, correo) is not None


CARACTERES_ESPECIALES = ('@', '$', '#', '!', '*', '&')


def validar_contrasena(contrasena: str) -> list:
    """Revisa que la contraseña sea segura (mismas reglas del proyecto base).
    Retorna la lista de errores: si está vacía, la contraseña es válida."""
    errores = []
    if len(contrasena) < 8:
        errores.append('Debe tener al menos 8 caracteres.')
    if not any(caracter.isdigit() for caracter in contrasena):
        errores.append('Debe tener al menos 1 número.')
    if not any(caracter.islower() for caracter in contrasena):
        errores.append('Debe tener al menos 1 minúscula.')
    if not any(caracter.isupper() for caracter in contrasena):
        errores.append('Debe tener al menos 1 mayúscula.')
    if not any(caracter in CARACTERES_ESPECIALES for caracter in contrasena):
        errores.append(f'Debe tener al menos 1 caracter especial: {", ".join(CARACTERES_ESPECIALES)}')
    return errores 