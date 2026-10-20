from negocio.negocio_tarjetas import (
    obtener_tarjeta,
    crear_tarjeta,
    modificar_tarjeta,
    eliminar_tarjeta,
    mover_tarjeta,
    asignar_responsable,
    cambiar_estado
)
from presentacion.presentacion_tableros import elegir_proyecto, mostrar_tablero, formatear_fecha
from presentacion.presentacion_proyectos import pedir_rut, mostrar_resultado
from auxiliares import (
    pedir_texto,
    pedir_entero,
    pedir_fecha,
    elegir_opcion,
    confirmar,
    estados_tarjeta,
    operacion_cancelada
)


def solicitar_datos_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_lista = pedir_entero('Id de la lista donde va la tarjeta: ')
    nombre = pedir_texto('Nombre de la tarjeta: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)
    fecha = pedir_fecha('Fecha límite dd-mm-aaaa (opcional, Enter para omitir): ')

    mostrar_resultado(*crear_tarjeta(id_lista, nombre, descripcion, fecha))


def solicitar_modificacion_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    tarjeta = obtener_tarjeta(pedir_entero('Id de la tarjeta a modificar: '))
    if not tarjeta:
        print('ERROR: No existe una tarjeta con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{tarjeta.nombtarj}]: ', obligatorio=False, largo_maximo=50)
    descripcion = pedir_texto(f'Descripción [{tarjeta.descriptarj or "-"}]: ', obligatorio=False, largo_maximo=150)
    fecha = pedir_fecha(f'Fecha límite dd-mm-aaaa [{formatear_fecha(tarjeta.fecha_vencimiento)}]: ')

    mostrar_resultado(*modificar_tarjeta(tarjeta.id_tarjeta, nombre, descripcion, fecha))


def solicitar_eliminar_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    tarjeta = obtener_tarjeta(pedir_entero('Id de la tarjeta a eliminar: '))
    if not tarjeta:
        print('ERROR: No existe una tarjeta con ese Id.\n')
        return

    if confirmar(f'¿Seguro que desea eliminar "{tarjeta.nombtarj}"?'):
        mostrar_resultado(*eliminar_tarjeta(tarjeta.id_tarjeta))
    else:
        print(operacion_cancelada)


def solicitar_mover_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta a mover: ')
    id_lista = pedir_entero('Id de la lista de destino: ')

    mostrar_resultado(*mover_tarjeta(id_tarjeta, id_lista))


def solicitar_responsable():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta: ')
    rut = pedir_rut('RUT del responsable (debe participar en el proyecto): ')

    mostrar_resultado(*asignar_responsable(id_tarjeta, rut))


def solicitar_cambio_estado():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta: ')
    print('Nuevo estado:')
    estado = elegir_opcion('Elija el estado: ', estados_tarjeta)

    mostrar_resultado(*cambiar_estado(id_tarjeta, estado)) 