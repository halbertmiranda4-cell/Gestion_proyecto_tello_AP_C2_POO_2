import sys
from negocio.negocio_usuarios import ServicioUsuarios
from presentacion.presentacion_usuarios import pedir_contrasena, solicitar_datos_usuario
from presentacion.presentacion_comun import mostrar_resultado
from auxiliares import menu_sesion, opcion_invalida, mensaje_error, pedir_texto


class Sesion:
    """Controla el inicio de sesión de la aplicación.

    Encapsulamiento: el usuario conectado y los intentos son privados.
    Desde afuera solo se puede consultar quién inició sesión (propiedad usuario_actual)."""

    MAXIMO_INTENTOS = 3
    __conectado = None   # atributo privado de clase: quién inició sesión en la aplicación

    def __init__(self):
        self.__servicio = ServicioUsuarios()
        self.__usuario = None
        self.__intentos = 0

    @property
    def usuario_actual(self):
        return self.__usuario

    @classmethod
    def usuario_conectado(cls):
        """Permite a otras pantallas saber quién inició sesión (ej: autor de un comentario)."""
        return cls.__conectado

    @property
    def iniciada(self) -> bool:
        return self.__usuario is not None

    def __intentar_ingreso(self):
        """Pide correo y contraseña una vez y los valida en la capa de negocio."""
        correo = pedir_texto('Correo: ', largo_maximo=100)
        contrasena = pedir_contrasena('Contraseña: ')
        exito, mensaje, usuario = self.__servicio.iniciar_sesion(correo, contrasena)
        mostrar_resultado(exito, mensaje)
        if exito:
            self.__usuario = usuario
            Sesion.__conectado = usuario
        else:
            self.__intentos += 1
            restantes = self.MAXIMO_INTENTOS - self.__intentos
            if restantes > 0:
                print(f'Le quedan {restantes} intento(s).\n')

    def iniciar(self) -> bool:
        """Muestra el menú de acceso hasta que el usuario entre, salga o agote los intentos."""
        print('\n--- Acceso ---')
        while not self.iniciada:
            if self.__intentos >= self.MAXIMO_INTENTOS:
                print('Demasiados intentos fallidos. Cerrando la aplicación.')
                return False
            for clave, valor in menu_sesion.items():
                print(f'[{clave}] - {valor}')
            try:
                match input('\nIngrese su opción [0-2]: '):
                    case '1':
                        self.__intentar_ingreso()
                    case '2':
                        solicitar_datos_usuario()
                        print('Ahora puede iniciar sesión con su correo y contraseña.\n')
                    case '0':
                        return False
                    case _:
                        print(opcion_invalida)
            except Exception as error:
                # Ej: MySQL apagado. Se muestra el error sin cerrar la aplicación.
                print(f'{mensaje_error}{error}\n')
        return True


def iniciar_sesion():
    """Punto de entrada del acceso: si no se inicia sesión, la app se cierra."""
    sesion = Sesion()
    if not sesion.iniciar():
        print('Saliendo...')
        sys.exit()
    return sesion.usuario_actual 