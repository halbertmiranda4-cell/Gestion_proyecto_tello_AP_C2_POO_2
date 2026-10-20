from prettytable import PrettyTable
from negocio.negocio_proyectos import (
    lista_proyectos,
    obtener_proyecto,
    crear_proyecto,
    modificar_proyecto,
    eliminar_proyecto,
    agregar_participante,
    lista_participantes
)
from auxiliares import (
    pedir_texto,
    pedir_entero,
    elegir_opcion,
    confirmar,
    validar_rut,
    roles_proyecto,
    operacion_cancelada
)


def mostrar_resultado(exito: bool, mensaje: str):
    print(('ERROR: ', 'OK: ')[exito] + mensaje + '\n')


def pedir_rut(mensaje: str) -> str:
    while True:
        rut = pedir_texto(mensaje)
        if validar_rut(rut):
            return rut
        print('RUT inválido. Intente nuevamente.')


def mostrar_proyectos() -> bool:
    """Muestra los proyectos habilitados. Retorna False si no hay ninguno."""
    tabla_proyectos = PrettyTable()
    tabla_proyectos.field_names = ['Id', 'Proyecto', 'Descripción', 'Creado', 'Participantes']
    tabla_proyectos = lista_proyectos(tabla_proyectos)
    if tabla_proyectos.rows:
        print(tabla_proyectos)
        return True
    print('No hay proyectos registrados.\n')
    return False


def solicitar_datos_proyecto():
    nombre = pedir_texto('Nombre del proyecto: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)
    rut_creador = pedir_rut('RUT del usuario que crea el proyecto: ')

    mostrar_resultado(*crear_proyecto(nombre, descripcion, rut_creador))


def solicitar_modificacion_proyecto():
    if not mostrar_proyectos():
        return
    proyecto = obtener_proyecto(pedir_entero('Id del proyecto a modificar: '))
    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{proyecto.nompro}]: ', obligatorio=False, largo_maximo=50)
    descripcion = pedir_texto(f'Descripción [{proyecto.descripcion or "-"}]: ', obligatorio=False, largo_maximo=150)

    mostrar_resultado(*modificar_proyecto(proyecto.id_proyecto, nombre, descripcion))


def solicitar_eliminar_proyecto():
    if not mostrar_proyectos():
        return
    proyecto = obtener_proyecto(pedir_entero('Id del proyecto a eliminar: '))
    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return

    print(f'Se eliminará el proyecto "{proyecto.nompro}" junto con el acceso a su tablero.')
    if confirmar('¿Continuar?'):
        mostrar_resultado(*eliminar_proyecto(proyecto.id_proyecto))
    else:
        print(operacion_cancelada)


def solicitar_participante():
    if not mostrar_proyectos():
        return
    id_proyecto = pedir_entero('Id del proyecto: ')
    rut = pedir_rut('RUT del usuario a agregar: ')
    print('Rol del participante:')
    rol = elegir_opcion('Elija el rol: ', roles_proyecto)

    mostrar_resultado(*agregar_participante(id_proyecto, rut, rol))


def mostrar_participantes():
    if not mostrar_proyectos():
        return
    id_proyecto = pedir_entero('Id del proyecto: ')

    tabla_participantes = PrettyTable()
    tabla_participantes.field_names = ['Nombre', 'RUT', 'Rol', 'Ingreso']
    proyecto, tabla_participantes = lista_participantes(id_proyecto, tabla_participantes)

    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
    elif tabla_participantes.rows:
        print(f'\nParticipantes de "{proyecto.nompro}":')
        print(tabla_participantes)
    else:
        print('El proyecto no tiene participantes.\n') 