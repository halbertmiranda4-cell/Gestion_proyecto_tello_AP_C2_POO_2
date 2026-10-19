from prettytable import PrettyTable
from negocio.negocio_proyectos import lista_proyectos, crear_proyecto, agregar_participante, lista_participantes
from auxiliares import pedir_texto, pedir_entero, elegir_opcion, validar_rut, roles_proyecto


def pedir_rut(mensaje: str) -> str:
    while True:
        rut = pedir_texto(mensaje)
        if validar_rut(rut):
            return rut
        print('RUT inválido. Intente nuevamente.')


def mostrar_proyectos():
    tabla_proyectos = PrettyTable()
    tabla_proyectos.field_names = ['Id', 'Proyecto', 'Descripción', 'Creado', 'Participantes']
    tabla_proyectos = lista_proyectos(tabla_proyectos)
    if tabla_proyectos.rows:
        print(tabla_proyectos)
    else:
        print('No hay proyectos registrados.\n')


def solicitar_datos_proyecto():
    nombre = pedir_texto('Nombre del proyecto: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)
    rut_creador = pedir_rut('RUT del usuario que crea el proyecto: ')

    exito, mensaje = crear_proyecto(nombre, descripcion, rut_creador)
    print(('ERROR: ', 'OK: ')[exito] + mensaje + '\n')


def solicitar_participante():
    mostrar_proyectos()
    id_proyecto = pedir_entero('Id del proyecto: ')
    rut = pedir_rut('RUT del usuario a agregar: ')
    print('Rol del participante:')
    rol = elegir_opcion('Elija el rol: ', roles_proyecto)

    exito, mensaje = agregar_participante(id_proyecto, rut, rol)
    print(('ERROR: ', 'OK: ')[exito] + mensaje + '\n')


def mostrar_participantes():
    mostrar_proyectos()
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