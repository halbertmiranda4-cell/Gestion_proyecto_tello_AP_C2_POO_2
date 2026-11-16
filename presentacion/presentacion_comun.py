from auxiliares import pedir_texto, confirmar, validar_rut, operacion_cancelada


def mostrar_resultado(exito: bool, mensaje: str):
    print(('ERROR: ', 'OK: ')[exito] + mensaje + '\n')


def pedir_rut(mensaje: str) -> str:
    while True:
        rut = pedir_texto(mensaje)
        if validar_rut(rut):
            return rut
        print('RUT inválido. Intente nuevamente.')


def formatear_fecha(fecha) -> str:
    return fecha.strftime('%d-%m-%Y') if fecha else '-'


def solicitar_eliminacion(servicio, id_registro: int, pregunta: str):
    """Polimorfismo: recibe CUALQUIER servicio (usuarios, proyectos, listas, tarjetas...)
    y llama a su eliminar(). Esta función no sabe ni le importa cuál es:
    cada clase responde a eliminar() con su propia regla."""
    if confirmar(pregunta):
        mostrar_resultado(*servicio.eliminar(id_registro))
    else:
        print(operacion_cancelada) 