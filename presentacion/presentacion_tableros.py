from prettytable import PrettyTable
from negocio.negocio_tableros import (
    crear_tablero,
    crear_lista,
    obtener_lista,
    modificar_lista,
    eliminar_lista,
    obtener_tablero,
    nombre_responsable,
    esta_vencida
)
from presentacion.presentacion_proyectos import mostrar_proyectos, mostrar_resultado
from auxiliares import pedir_texto, pedir_entero, confirmar, operacion_cancelada


def elegir_proyecto() -> int:
    mostrar_proyectos()
    return pedir_entero('Id del proyecto: ')


def formatear_fecha(fecha) -> str:
    return fecha.strftime('%d-%m-%Y') if fecha else '-'


def mostrar_tablero(id_proyecto: int) -> bool:
    """Muestra cada lista con sus tarjetas. Retorna False si no hay tablero que mostrar."""
    proyecto, tablero, listas = obtener_tablero(id_proyecto)
    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return False
    if not tablero:
        print(f'"{proyecto.nompro}" aún no tiene tablero.\n')
        return False

    print(f'\n=== {tablero.nomtab} · {proyecto.nompro} ===')
    if not listas:
        print('El tablero no tiene listas.\n')
        return True

    for lista in listas:
        print(f'\n[Lista Id {lista.id_lista}] {lista.nomblist} ({len(lista.tarjetas)} tarjetas)')
        if not lista.tarjetas:
            print('   (vacía)')
            continue
        tabla = PrettyTable()
        tabla.field_names = ['Id', 'Tarjeta', 'Estado', 'Vence', 'Responsable']
        for tarjeta in lista.tarjetas:
            vence = formatear_fecha(tarjeta.fecha_vencimiento)
            if esta_vencida(tarjeta):
                vence += ' VENCIDA'
            tabla.add_row([tarjeta.id_tarjeta, tarjeta.nombtarj, tarjeta.estado, vence, nombre_responsable(tarjeta)])
        print(tabla)
    print()
    return True


def ver_tablero():
    mostrar_tablero(elegir_proyecto())


def solicitar_datos_tablero():
    id_proyecto = elegir_proyecto()
    nombre = pedir_texto('Nombre del tablero: ', largo_maximo=50)

    mostrar_resultado(*crear_tablero(id_proyecto, nombre))


def solicitar_datos_lista():
    id_proyecto = elegir_proyecto()
    nombre = pedir_texto('Nombre de la lista: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)

    mostrar_resultado(*crear_lista(id_proyecto, nombre, descripcion))


def solicitar_modificacion_lista():
    if not mostrar_tablero(elegir_proyecto()):
        return
    lista = obtener_lista(pedir_entero('Id de la lista a modificar: '))
    if not lista:
        print('ERROR: No existe una lista con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{lista.nomblist}]: ', obligatorio=False, largo_maximo=50)
    descripcion = pedir_texto(f'Descripción [{lista.descriplist or "-"}]: ', obligatorio=False, largo_maximo=150)

    mostrar_resultado(*modificar_lista(lista.id_lista, nombre, descripcion))


def solicitar_eliminar_lista():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_lista = pedir_entero('Id de la lista a eliminar: ')
    if confirmar('¿Seguro que desea eliminar la lista?'):
        mostrar_resultado(*eliminar_lista(id_lista))
    else:
        print(operacion_cancelada) 