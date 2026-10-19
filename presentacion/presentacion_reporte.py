from prettytable import PrettyTable
from negocio.negocio_reporte import reporte_avance
from presentacion.presentacion_tableros import elegir_proyecto, formatear_fecha
from negocio.negocio_tableros import nombre_responsable


def barra_progreso(porcentaje: int, largo: int = 20) -> str:
    llenos = round(porcentaje * largo / 100)
    return '[' + '#' * llenos + '-' * (largo - llenos) + ']'


def mostrar_reporte():
    exito, mensaje, datos = reporte_avance(elegir_proyecto())
    if not exito:
        print('ERROR: ' + mensaje + '\n')
        return

    print(f'\n=== Reporte de avance · {datos["proyecto"].nompro} ===')
    if datos['total'] == 0:
        print('El tablero aún no tiene tarjetas.\n')
        return

    print(f'{barra_progreso(datos["porcentaje"])} {datos["porcentaje"]}%  '
          f'({datos["completadas"]} de {datos["total"]} tarjetas completadas)\n')

    tabla_estados = PrettyTable()
    tabla_estados.field_names = ['Estado', 'Tarjetas']
    for estado, cantidad in datos['por_estado'].items():
        tabla_estados.add_row([estado, cantidad])
    print(tabla_estados)

    tabla_responsables = PrettyTable()
    tabla_responsables.field_names = ['Responsable', 'Asignadas', 'Completadas']
    for responsable, conteo in datos['por_responsable'].items():
        tabla_responsables.add_row([responsable, conteo['total'], conteo['completadas']])
    print(tabla_responsables)

    if datos['vencidas']:
        print(f'\nTarjetas vencidas ({len(datos["vencidas"])}):')
        tabla_vencidas = PrettyTable()
        tabla_vencidas.field_names = ['Id', 'Tarjeta', 'Venció', 'Responsable']
        for tarjeta in datos['vencidas']:
            tabla_vencidas.add_row([tarjeta.id_tarjeta, tarjeta.nombtarj,
                                    formatear_fecha(tarjeta.fecha_vencimiento), nombre_responsable(tarjeta)])
        print(tabla_vencidas)
    else:
        print('\nNo hay tarjetas vencidas.')
    print()