from prettytable import PrettyTable
from negocio.negocio_proyectos import ServicioProyectos
from presentacion.presentacion_comun import mostrar_resultado, pedir_rut, solicitar_eliminacion
from auxiliares import pedir_texto, pedir_entero, elegir_opcion, roles_proyecto


servicio_proyectos = ServicioProyectos()


def mostrar_proyectos() -> bool:
    """Muestra los proyectos habilitados. Retorna False si no hay ninguno."""
    proyectos = servicio_proyectos.listar()
    if not proyectos:
        print('No hay proyectos registrados.\n')
        return False

    tabla_proyectos = PrettyTable()
    tabla_proyectos.field_names = ['Id', 'Proyecto', 'Descripción', 'Creado', 'Participantes']
    for proyecto in proyectos:
        tabla_proyectos.add_row([proyecto.id_proyecto, proyecto.nompro, proyecto.descripcion or '-',
                                 proyecto.fecha_creacion, proyecto.participantes])
    print(tabla_proyectos)
    return True


def solicitar_datos_proyecto():
    nombre = pedir_texto('Nombre del proyecto: ', largo_maximo=50)
    descripcion = pedir_texto('Descripción (opcional, Enter para omitir): ', obligatorio=False, largo_maximo=150)
    rut_creador = pedir_rut('RUT del usuario que crea el proyecto: ')

    mostrar_resultado(*servicio_proyectos.crear(nombre, descripcion, rut_creador))


def solicitar_modificacion_proyecto():
    if not mostrar_proyectos():
        return
    proyecto = servicio_proyectos.obtener(pedir_entero('Id del proyecto a modificar: '))
    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar.')
    nombre = pedir_texto(f'Nombre [{proyecto.nompro}]: ', obligatorio=False, largo_maximo=50)
    descripcion = pedir_texto(f'Descripción [{proyecto.descripcion or "-"}]: ', obligatorio=False, largo_maximo=150)

    mostrar_resultado(*servicio_proyectos.modificar(proyecto.id_proyecto, nombre, descripcion))


def solicitar_eliminar_proyecto():
    if not mostrar_proyectos():
        return
    proyecto = servicio_proyectos.obtener(pedir_entero('Id del proyecto a eliminar: '))
    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return

    rut = pedir_rut('Su RUT (solo un administrador del proyecto puede eliminarlo): ')
    permitido, mensaje = servicio_proyectos.verificar_permiso_eliminar(proyecto.id_proyecto, rut)
    if not permitido:
        mostrar_resultado(False, mensaje)
        return

    print(f'Se eliminará el proyecto "{proyecto.nompro}" junto con el acceso a su tablero.')
    solicitar_eliminacion(servicio_proyectos, proyecto.id_proyecto, '¿Continuar?')


def solicitar_participante():
    if not mostrar_proyectos():
        return
    id_proyecto = pedir_entero('Id del proyecto: ')
    rut_solicitante = pedir_rut('Su RUT (debe ser administrador del proyecto): ')
    rut = pedir_rut('RUT del usuario a agregar: ')
    print('Rol del participante:')
    rol = elegir_opcion('Elija el rol: ', roles_proyecto)

    mostrar_resultado(*servicio_proyectos.agregar_participante(id_proyecto, rut_solicitante, rut, rol))


def mostrar_participantes():
    if not mostrar_proyectos():
        return
    proyecto, participantes = servicio_proyectos.listar_participantes(pedir_entero('Id del proyecto: '))

    if not proyecto:
        print('ERROR: No existe un proyecto con ese Id.\n')
        return
    if not participantes:
        print('El proyecto no tiene participantes.\n')
        return

    tabla_participantes = PrettyTable()
    tabla_participantes.field_names = ['Nombre', 'RUT', 'Rol', 'Permisos', 'Ingreso']
    for participante in participantes:
        usuario = participante.id_usuario
        tabla_participantes.add_row([usuario.nombre, usuario.rut, participante.rol,
                                     participante.rol_actual.permisos(), participante.fecha_ingreso])
    print(f'\nParticipantes de "{proyecto.nompro}":')
    print(tabla_participantes) 