from prettytable import PrettyTable
from datos.modelos.models import Proyecto
from datos.repositorios.repositorio_base import guardar_registro
from datos.repositorios.repositorio_usuarios import buscar_usuario_por_rut
from datos.repositorios.repositorio_proyectos import (
    listado_proyectos,
    buscar_proyecto_por_id,
    buscar_proyecto_por_nombre,
    buscar_participacion,
    listado_participantes,
    guardar_proyecto_con_administrador,
    guardar_participante
)
from auxiliares import validar_rut, formatear_rut, roles_proyecto


def lista_proyectos(tabla_proyectos: PrettyTable):
    proyectos = listado_proyectos()
    if proyectos:
        for proyecto in proyectos:
            tabla_proyectos.add_row([proyecto.id_proyecto, proyecto.nompro, proyecto.descripcion or '-',
                                     proyecto.fecha_creacion, proyecto.participantes])
    return tabla_proyectos


def obtener_proyecto(id_proyecto: int):
    return buscar_proyecto_por_id(id_proyecto)


def buscar_usuario(rut: str):
    """Retorna el usuario con ese RUT, o None si el RUT es inválido o no existe."""
    if not validar_rut(rut):
        return None
    return buscar_usuario_por_rut(formatear_rut(rut))


def crear_proyecto(nombre: str, descripcion: str, rut_creador: str):
    """Crea el proyecto y deja a quien lo crea como administrador.
    Retorna (exito, mensaje)."""
    nombre = nombre.strip()

    # Reglas de negocio
    if not nombre:
        return False, 'El nombre del proyecto es obligatorio.'
    if buscar_proyecto_por_nombre(nombre):
        return False, 'Ya existe un proyecto con ese nombre.'
    creador = buscar_usuario(rut_creador)
    if not creador:
        return False, 'No existe un usuario con ese RUT.'
    if not creador.habilitado:
        return False, f'{creador.nombre} está deshabilitado y no puede crear proyectos.'

    nuevo_proyecto = Proyecto()
    nuevo_proyecto.nompro = nombre
    nuevo_proyecto.descripcion = descripcion.strip() or None
    nuevo_proyecto.habilitado = 1

    if guardar_proyecto_con_administrador(nuevo_proyecto, creador):
        return True, f'Proyecto "{nombre}" creado. {creador.nombre} quedó como administrador.'
    return False, 'No se pudo crear el proyecto.'


def modificar_proyecto(id_proyecto: int, nombre: str, descripcion: str):
    """Modifica nombre y/o descripción. Un campo vacío significa "no cambiar".
    Retorna (exito, mensaje)."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return False, 'No existe un proyecto con ese Id.'

    cambios = []

    nombre = nombre.strip()
    if nombre and nombre != proyecto.nompro:
        otro = buscar_proyecto_por_nombre(nombre)
        if otro and otro.id_proyecto != proyecto.id_proyecto:
            return False, 'Ya existe otro proyecto con ese nombre.'
        proyecto.nompro = nombre
        cambios.append('nombre')

    descripcion = descripcion.strip()
    if descripcion and descripcion != proyecto.descripcion:
        proyecto.descripcion = descripcion
        cambios.append('descripción')

    if not cambios:
        return False, 'No se ingresó ningún cambio.'
    if guardar_registro(proyecto):
        return True, f'Proyecto "{proyecto.nompro}" actualizado ({", ".join(cambios)}).'
    return False, 'No se pudo modificar el proyecto.'


def eliminar_proyecto(id_proyecto: int):
    """Borrado lógico: el proyecto deja de aparecer, pero sus datos se conservan.
    Retorna (exito, mensaje)."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return False, 'No existe un proyecto con ese Id.'

    proyecto.habilitado = 0
    if guardar_registro(proyecto):
        return True, f'Proyecto "{proyecto.nompro}" eliminado.'
    return False, 'No se pudo eliminar el proyecto.'


def agregar_participante(id_proyecto: int, rut: str, rol: str):
    """Agrega un usuario a un proyecto con un rol. Retorna (exito, mensaje)."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return False, 'No existe un proyecto con ese Id.'
    usuario = buscar_usuario(rut)
    if not usuario:
        return False, 'No existe un usuario con ese RUT.'
    if not usuario.habilitado:
        return False, f'{usuario.nombre} está deshabilitado y no puede unirse a proyectos.'
    if rol not in roles_proyecto:
        return False, 'El rol no es válido.'
    if buscar_participacion(usuario, proyecto):
        return False, f'{usuario.nombre} ya participa en este proyecto.'

    if guardar_participante(usuario, proyecto, rol):
        return True, f'{usuario.nombre} agregado a "{proyecto.nompro}" como {rol}.'
    return False, 'No se pudo agregar el participante.'


def lista_participantes(id_proyecto: int, tabla_participantes: PrettyTable):
    """Retorna (proyecto, tabla). Si el proyecto no existe, proyecto es None."""
    proyecto = buscar_proyecto_por_id(id_proyecto)
    if not proyecto:
        return None, tabla_participantes
    participantes = listado_participantes(proyecto)
    if participantes:
        for participante in participantes:
            usuario = participante.id_usuario
            tabla_participantes.add_row([usuario.nombre, usuario.rut, participante.rol, participante.fecha_ingreso])
    return proyecto, tabla_participantes 