import sys
from auxiliares import (
    nombre_aplicacion,
    version_aplicacion,
    menu_superior,
    menu_usuarios,
    menu_proyectos,
    menu_tableros,
    menu_tarjetas,
    menu_etiquetas,
    opcion_invalida,
    menu_anterior,
    mensaje_error
)
from presentacion.presentacion_usuarios import (
    mostrar_usuarios,
    solicitar_datos_usuario,
    solicitar_modificacion_usuario,
    solicitar_deshabilitar_usuario,
    solicitar_habilitar_usuario
)
from presentacion.presentacion_proyectos import (
    mostrar_proyectos,
    solicitar_datos_proyecto,
    solicitar_modificacion_proyecto,
    solicitar_eliminar_proyecto,
    solicitar_participante,
    mostrar_participantes
)
from presentacion.presentacion_tableros import (
    ver_tablero,
    solicitar_datos_tablero,
    solicitar_datos_lista,
    solicitar_modificacion_lista,
    solicitar_eliminar_lista
)
from presentacion.presentacion_tarjetas import (
    solicitar_datos_tarjeta,
    solicitar_modificacion_tarjeta,
    solicitar_eliminar_tarjeta,
    solicitar_mover_tarjeta,
    solicitar_responsable,
    solicitar_cambio_estado
)
from presentacion.presentacion_comentarios import (
    solicitar_comentario,
    ver_comentarios,
    solicitar_eliminar_comentario
)
from presentacion.presentacion_etiquetas import (
    ver_etiquetas,
    solicitar_datos_etiqueta,
    solicitar_modificacion_etiqueta,
    solicitar_eliminar_etiqueta,
    solicitar_asignar_etiqueta,
    solicitar_quitar_etiqueta
)
from presentacion.presentacion_reporte import mostrar_reporte
from presentacion.presentacion_sesion import iniciar_sesion


class Menu:
    """Un menú de consola: muestra opciones y ejecuta la acción elegida.
    Encapsulamiento: las opciones y acciones son privadas; desde fuera solo se llama a ejecutar()."""

    def __init__(self, titulo: str, opciones: dict, acciones: dict):
        self.__titulo = titulo
        self.__opciones = opciones     # {'1': 'texto', ..., '0': 'Volver'}
        self.__acciones = acciones     # {'1': funcion o Menu, ...}

    @property
    def titulo(self) -> str:
        return self.__titulo

    def _mostrar_encabezado(self):
        print(f'\n--- {self.__titulo} ---')

    def _salir(self):
        print(menu_anterior)

    def __mostrar_opciones(self):
        for clave, valor in self.__opciones.items():
            print(f'[{clave}] - {valor}')

    @staticmethod
    def __ejecutar_accion(accion):
        """Si ocurre un error inesperado (por ejemplo, se pierde la conexión con MySQL),
        lo muestra y vuelve al menú en vez de cerrar la app."""
        try:
            accion()
        except Exception as error:
            print(f'{mensaje_error}{error}\n')

    def ejecutar(self):
        while True:
            self._mostrar_encabezado()
            self.__mostrar_opciones()
            opcion = input(f'\nIngrese su opción [0-{len(self.__acciones)}]: ')
            if opcion == '0':
                self._salir()
                break
            accion = self.__acciones.get(opcion)
            if isinstance(accion, Menu):
                accion.ejecutar()                 # un submenú es también un Menu
            elif accion:
                self.__ejecutar_accion(accion)
            else:
                print(opcion_invalida)


class MenuPrincipal(Menu):
    """Herencia: es un Menu, pero muestra el nombre y versión una sola vez y al salir cierra la app.
    Polimorfismo: sobrescribe _mostrar_encabezado() y _salir()."""

    def ejecutar(self):
        print(f'\n{self.titulo}')
        print('=' * len(self.titulo) + '\n')
        super().ejecutar()

    def _mostrar_encabezado(self):
        pass   # el título ya se mostró al iniciar

    def _salir(self):
        print('Saliendo...')
        sys.exit()


def menu_principal():
    print(f'\n{nombre_aplicacion} - {version_aplicacion}')
    usuario = iniciar_sesion()   # si no inicia sesión, la app se cierra aquí

    MenuPrincipal(f'{nombre_aplicacion} - {version_aplicacion} · Sesión: {usuario.nombre}', menu_superior, {
        '1': Menu('Gestión Usuarios', menu_usuarios, {
            '1': mostrar_usuarios,
            '2': solicitar_datos_usuario,
            '3': solicitar_modificacion_usuario,
            '4': solicitar_deshabilitar_usuario,
            '5': solicitar_habilitar_usuario
        }),
        '2': Menu('Gestión Proyectos', menu_proyectos, {
            '1': mostrar_proyectos,
            '2': solicitar_datos_proyecto,
            '3': solicitar_modificacion_proyecto,
            '4': solicitar_eliminar_proyecto,
            '5': solicitar_participante,
            '6': mostrar_participantes
        }),
        '3': Menu('Gestión Tableros y Listas', menu_tableros, {
            '1': ver_tablero,
            '2': solicitar_datos_tablero,
            '3': solicitar_datos_lista,
            '4': solicitar_modificacion_lista,
            '5': solicitar_eliminar_lista
        }),
        '4': Menu('Gestión Tarjetas', menu_tarjetas, {
            '1': solicitar_datos_tarjeta,
            '2': solicitar_modificacion_tarjeta,
            '3': solicitar_eliminar_tarjeta,
            '4': solicitar_mover_tarjeta,
            '5': solicitar_responsable,
            '6': solicitar_cambio_estado,
            '7': solicitar_comentario,
            '8': ver_comentarios,
            '9': solicitar_eliminar_comentario
        }),
        '5': Menu('Gestión Etiquetas', menu_etiquetas, {
            '1': ver_etiquetas,
            '2': solicitar_datos_etiqueta,
            '3': solicitar_modificacion_etiqueta,
            '4': solicitar_eliminar_etiqueta,
            '5': solicitar_asignar_etiqueta,
            '6': solicitar_quitar_etiqueta
        }),
        '6': mostrar_reporte
    }).ejecutar() 