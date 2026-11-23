from prettytable import PrettyTable
from negocio.negocio_etiquetas import ServicioEtiquetas
from presentacion.presentacion_tableros import elegir_proyecto, mostrar_tablero
from presentacion.presentacion_comun import mostrar_resultado, solicitar_eliminacion
from auxiliares import pedir_texto, pedir_entero, elegir_opcion, confirmar, colores_etiqueta


servicio_etiquetas = ServicioEtiquetas()


def mostrar_etiquetas(id_proyecto: int) -> bool:
    """Muestra las etiquetas de un proyecto. Retorna False si no hay ninguna."""
    proyecto, etiquetas = servicio_etiquetas.listar_por_proyecto(id_proyecto)
    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return False
    if not etiquetas:
        print(f'"{proyecto.nompro}" no tiene etiquetas.\n')
        return False

    tabla = PrettyTable()
    tabla.field_names = ['Id', 'Etiqueta', 'Color']
    for etiqueta in etiquetas:
        tabla.add_row([etiqueta.id_etiqueta, etiqueta.nometiq, etiqueta.color])
    print(f'\nEtiquetas de "{proyecto.nompro}":')
    print(tabla)
    return True


def ver_etiquetas():
    mostrar_etiquetas(elegir_proyecto())


def solicitar_datos_etiqueta():
    id_proyecto = elegir_proyecto()
    nombre = pedir_texto('Nombre de la etiqueta: ', largo_maximo=30)
    print('Color:')
    color = elegir_opcion('Elija el color: ', colores_etiqueta)

    mostrar_resultado(*servicio_etiquetas.crear(id_proyecto, nombre, color))


def solicitar_modificacion_etiqueta():
    if not mostrar_etiquetas(elegir_proyecto()):
        return
    etiqueta = servicio_etiquetas.obtener(pedir_entero('Id de la etiqueta a modificar: '))
    if not etiqueta:
        print('ERROR: No existe una etiqueta con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{etiqueta.nometiq}]: ', obligatorio=False, largo_maximo=30)
    color = ''
    if confirmar(f'¿Desea cambiar el color ({etiqueta.color})?'):
        color = elegir_opcion('Elija el color: ', colores_etiqueta)

    mostrar_resultado(*servicio_etiquetas.modificar(etiqueta.id_etiqueta, nombre, color))


def solicitar_eliminar_etiqueta():
    if not mostrar_etiquetas(elegir_proyecto()):
        return
    id_etiqueta = pedir_entero('Id de la etiqueta a eliminar: ')
    solicitar_eliminacion(servicio_etiquetas, id_etiqueta, '¿Seguro que desea eliminar la etiqueta?')


def _pedir_tarjeta_y_etiqueta():
    """Muestra el tablero y las etiquetas del proyecto y pide ambos Id. Retorna (id_tarjeta, id_etiqueta) o None."""
    id_proyecto = elegir_proyecto()
    if not mostrar_tablero(id_proyecto) or not mostrar_etiquetas(id_proyecto):
        return None
    return pedir_entero('Id de la tarjeta: '), pedir_entero('Id de la etiqueta: ')


def solicitar_asignar_etiqueta():
    ids = _pedir_tarjeta_y_etiqueta()
    if ids:
        mostrar_resultado(*servicio_etiquetas.asignar(*ids))


def solicitar_quitar_etiqueta():
    ids = _pedir_tarjeta_y_etiqueta()
    if ids:
        mostrar_resultado(*servicio_etiquetas.quitar(*ids))