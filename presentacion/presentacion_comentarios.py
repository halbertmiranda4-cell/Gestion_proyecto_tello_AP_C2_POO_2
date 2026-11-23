from prettytable import PrettyTable
from negocio.negocio_comentarios import ServicioComentarios
from presentacion.presentacion_tableros import elegir_proyecto, mostrar_tablero
from presentacion.presentacion_comun import mostrar_resultado, formatear_fecha, solicitar_eliminacion
from presentacion.presentacion_sesion import Sesion
from auxiliares import pedir_texto, pedir_entero


servicio_comentarios = ServicioComentarios()


def mostrar_comentarios(id_tarjeta: int) -> bool:
    """Muestra los comentarios de una tarjeta. Retorna False si no hay ninguno."""
    tarjeta, comentarios = servicio_comentarios.listar_por_tarjeta(id_tarjeta)
    if not tarjeta:
        print('ERROR: No existe una tarjeta con ese Id.\n')
        return False
    if not comentarios:
        print(f'"{tarjeta}" no tiene comentarios.\n')
        return False

    tabla = PrettyTable()
    tabla.field_names = ['Id', 'Fecha', 'Autor', 'Comentario']
    tabla.align['Comentario'] = 'l'
    for comentario in comentarios:
        tabla.add_row([comentario.id_comentario, formatear_fecha(comentario.fecha_creacion),
                       comentario.id_usuario.nombre, comentario.texto])
    print(f'\nComentarios de "{tarjeta}":')
    print(tabla)
    return True


def solicitar_comentario():
    if not mostrar_tablero(elegir_proyecto()):
        return
    id_tarjeta = pedir_entero('Id de la tarjeta a comentar: ')
    texto = pedir_texto('Comentario: ', largo_maximo=500)
    # El autor es siempre quien inició sesión
    mostrar_resultado(*servicio_comentarios.crear(id_tarjeta, Sesion.usuario_conectado(), texto))


def ver_comentarios():
    if not mostrar_tablero(elegir_proyecto()):
        return
    mostrar_comentarios(pedir_entero('Id de la tarjeta: '))


def solicitar_eliminar_comentario():
    if not mostrar_tablero(elegir_proyecto()):
        return
    if not mostrar_comentarios(pedir_entero('Id de la tarjeta: ')):
        return
    id_comentario = pedir_entero('Id del comentario a eliminar: ')
    permitido, mensaje = servicio_comentarios.verificar_autor(id_comentario, Sesion.usuario_conectado())
    if not permitido:
        mostrar_resultado(False, mensaje)
        return
    solicitar_eliminacion(servicio_comentarios, id_comentario, '¿Seguro que desea eliminar el comentario?') 