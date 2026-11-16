from prettytable import PrettyTable
from negocio.negocio_tableros import ServicioTableros, ServicioListas
from presentacion.presentacion_proyectos import mostrar_proyectos
from presentacion.presentacion_comun import mostrar_resultado, formatear_fecha, solicitar_eliminacion
from auxiliares import pedir_texto, pedir_entero


servicio_tableros = ServicioTableros()
servicio_listas = ServicioListas()


def elegir_proyecto() -> int:
    mostrar_proyectos()
    return pedir_entero('Id del proyecto: ')


def mostrar_tablero(id_proyecto: int) -> bool:
    """Muestra cada lista con sus tarjetas. Retorna False si no hay tablero que mostrar."""
    proyecto, tablero, listas = servicio_tableros.obtener_tablero(id_proyecto)
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
            if tarjeta.esta_vencida():
                vence += ' VENCIDA'
            tabla.add_row([tarjeta.id_tarjeta, tarjeta.nombre, tarjeta.estado_actual.etiqueta(), vence,
                           tarjeta.nombre_responsable])
        print(tabla)
    print()
    return True


def ver_tablero():
    mostrar_tablero(elegir_proyecto())


def solicitar_datos_tablero():
    id_proyecto = elegir_proyecto()
    nombre = pedir_texto('Nombre del tablero: ', largo_maximo=50)

    mostrar_resultado(*servicio_tableros.crear(id_proyecto, nombre))


def solicitar_datos_lista():
    id_proyecto = elegir_proyecto()
    nombre = pedir_texto('Nombre de la lista: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)

    mostrar_resultado(*servicio_listas.crear(id_proyecto, nombre, descripcion))


def solicitar_modificacion_lista():
    if not mostrar_tablero(elegir_proyecto()):
        return
    lista = servicio_listas.obtener(pedir_entero('Id de la lista a modificar: '))
    if not lista:
        print('ERROR: No existe una lista con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{lista.nomblist}]: ', obligatorio=False, largo_maximo=50)
    descripcion = pedir_texto(f'Descripción [{lista.descriplist or "-"}]: ', obligatorio=False, largo_maximo=150)

    mostrar_resultado(*servicio_listas.modificar(lista.id_lista, nombre, descripcion))


def solicitar_eliminar_lista():
    if not mostrar_tablero(elegir_proyecto()):
        return
    lista = servicio_listas.obtener(pedir_entero('Id de la lista a eliminar: '))
    if not lista:
        print('ERROR: No existe una lista con ese Id.\n')
        return
    # resumen() viene del padre ElementoTablero; nombre, tipo() y ubicacion() son de Lista
    solicitar_eliminacion(servicio_listas, lista.id_lista, f'¿Seguro que desea eliminar la {lista.resumen()}?') 