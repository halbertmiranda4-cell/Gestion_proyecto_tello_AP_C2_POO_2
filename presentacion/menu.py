import sys
from auxiliares import (
    nombre_aplicacion,
    version_aplicacion,
    menu_superior,
    menu_usuarios,
    menu_proyectos,
    menu_tableros,
    menu_tarjetas,
    opcion_invalida,
    menu_anterior
)
from presentacion.presentacion_usuarios import mostrar_usuarios, solicitar_datos_usuario
from presentacion.presentacion_proyectos import (
    mostrar_proyectos,
    solicitar_datos_proyecto,
    solicitar_participante,
    mostrar_participantes
)
from presentacion.presentacion_tableros import ver_tablero, solicitar_datos_tablero, solicitar_datos_lista
from presentacion.presentacion_tarjetas import (
    solicitar_datos_tarjeta,
    solicitar_mover_tarjeta,
    solicitar_responsable,
    solicitar_cambio_estado
)
from presentacion.presentacion_reporte import mostrar_reporte


def mostrar_opciones(menu: dict):
    for clave, valor in menu.items():
        print(f'[{clave}] - {valor}')


def sub_menu(titulo: str, opciones: dict, acciones: dict):
    """Muestra un submenú y ejecuta la función asociada a cada opción.
    acciones: {'1': funcion, '2': funcion, ...}. La opción '0' vuelve."""
    while True:
        print(f'\n--- {titulo} ---')
        mostrar_opciones(opciones)
        opcion = input(f'\nIngrese su opción [0-{len(acciones)}]: ')
        if opcion == '0':
            print(menu_anterior)
            break
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print(opcion_invalida)


def menu_principal():
    titulo = f'{nombre_aplicacion} - {version_aplicacion}'
    print(f'\n{titulo}')
    print('=' * len(titulo) + '\n')

    while True:
        mostrar_opciones(menu_superior)
        opcion_usuario = input('\nIngrese su opción [0-5]: ')

        match opcion_usuario:
            case '1':
                sub_menu('Gestión Usuarios', menu_usuarios, {
                    '1': mostrar_usuarios,
                    '2': solicitar_datos_usuario
                })
            case '2':
                sub_menu('Gestión Proyectos', menu_proyectos, {
                    '1': mostrar_proyectos,
                    '2': solicitar_datos_proyecto,
                    '3': solicitar_participante,
                    '4': mostrar_participantes
                })
            case '3':
                sub_menu('Gestión Tableros y Listas', menu_tableros, {
                    '1': ver_tablero,
                    '2': solicitar_datos_tablero,
                    '3': solicitar_datos_lista
                })
            case '4':
                sub_menu('Gestión Tarjetas', menu_tarjetas, {
                    '1': solicitar_datos_tarjeta,
                    '2': solicitar_mover_tarjeta,
                    '3': solicitar_responsable,
                    '4': solicitar_cambio_estado
                })
            case '5':
                mostrar_reporte()
            case '0':
                print('Saliendo...')
                sys.exit()
            case _:
                print(opcion_invalida)