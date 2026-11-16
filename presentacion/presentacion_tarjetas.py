from negocio.negocio_tarjetas import ServicioTarjetas
from presentacion.presentacion_tableros import elegir_proyecto, mostrar_tablero
from presentacion.presentacion_comun import mostrar_resultado, pedir_rut, formatear_fecha, solicitar_eliminacion
from auxiliares import pedir_texto, pedir_entero, pedir_fecha, elegir_opcion, estados_tarjeta


servicio_tarjetas = ServicioTarjetas()


def solicitar_datos_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_lista = pedir_entero('Id de la lista donde va la tarjeta: ')
    nombre = pedir_texto('Nombre de la tarjeta: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)
    fecha = pedir_fecha('Fecha límite dd-mm-aaaa (opcional, Enter para omitir): ')

    mostrar_resultado(*servicio_tarjetas.crear(id_lista, nombre, descripcion, fecha))


def solicitar_modificacion_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    tarjeta = servicio_tarjetas.obtener(pedir_entero('Id de la tarjeta a modificar: '))
    if not tarjeta:
        print('ERROR: No existe una tarjeta con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{tarjeta.nombtarj}]: ', obligatorio=False, largo_maximo=50)
    descripcion = pedir_texto(f'Descripción [{tarjeta.descriptarj or "-"}]: ', obligatorio=False, largo_maximo=150)
    fecha = pedir_fecha(f'Fecha límite dd-mm-aaaa [{formatear_fecha(tarjeta.fecha_vencimiento)}]: ')

    mostrar_resultado(*servicio_tarjetas.modificar(tarjeta.id_tarjeta, nombre, descripcion, fecha))


def solicitar_eliminar_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    tarjeta = servicio_tarjetas.obtener(pedir_entero('Id de la tarjeta a eliminar: '))
    if not tarjeta:
        print('ERROR: No existe una tarjeta con ese Id.\n')
        return

    # resumen() viene del padre ElementoTablero; nombre, tipo() y ubicacion() son de Tarjeta
    solicitar_eliminacion(servicio_tarjetas, tarjeta.id_tarjeta, f'¿Seguro que desea eliminar la {tarjeta.resumen()}?')


def solicitar_mover_tarjeta():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta a mover: ')
    id_lista = pedir_entero('Id de la lista de destino: ')

    mostrar_resultado(*servicio_tarjetas.mover(id_tarjeta, id_lista))


def solicitar_responsable():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta: ')
    rut = pedir_rut('RUT del responsable (debe participar en el proyecto): ')

    mostrar_resultado(*servicio_tarjetas.asignar_responsable(id_tarjeta, rut))


def solicitar_cambio_estado():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta: ')
    print('Nuevo estado:')
    estado = elegir_opcion('Elija el estado: ', estados_tarjeta)

    mostrar_resultado(*servicio_tarjetas.cambiar_estado(id_tarjeta, estado)) 