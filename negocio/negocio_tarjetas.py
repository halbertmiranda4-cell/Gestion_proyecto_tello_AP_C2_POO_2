from datetime import date
from datos.modelos.models import Tarjeta
from datos.repositorios.repositorio_base import guardar_registro
from datos.repositorios.repositorio_tableros import buscar_lista_por_id
from datos.repositorios.repositorio_tarjetas import (
    buscar_tarjeta_por_id,
    siguiente_posicion_tarjeta,
    buscar_participante_por_rut
)
from auxiliares import validar_rut, formatear_rut, estados_tarjeta


def proyecto_de_tarjeta(tarjeta):
    return tarjeta.id_lista.id_tablero.id_proyecto


def obtener_tarjeta(id_tarjeta: int):
    return buscar_tarjeta_por_id(id_tarjeta)


def crear_tarjeta(id_lista: int, nombre: str, descripcion: str, fecha_vencimiento):
    """Crea una tarjeta al final de la lista. fecha_vencimiento: date o None.
    Retorna (exito, mensaje)."""
    lista = buscar_lista_por_id(id_lista)
    if not lista:
        return False, 'No existe una lista con ese Id.'
    if not nombre.strip():
        return False, 'El nombre de la tarjeta es obligatorio.'
    if fecha_vencimiento and fecha_vencimiento < date.today():
        return False, 'La fecha límite no puede ser anterior a hoy.'

    tarjeta = Tarjeta()
    tarjeta.nombtarj = nombre.strip()
    tarjeta.descriptarj = descripcion.strip() or None
    tarjeta.fecha_vencimiento = fecha_vencimiento
    tarjeta.estado = 'pendiente'
    tarjeta.id_lista = lista
    tarjeta.posicion = siguiente_posicion_tarjeta(lista)
    tarjeta.habilitado = 1
    if guardar_registro(tarjeta):
        return True, f'Tarjeta "{tarjeta.nombtarj}" creada en "{lista.nomblist}" (Id {tarjeta.id_tarjeta}).'
    return False, 'No se pudo crear la tarjeta.'


def modificar_tarjeta(id_tarjeta: int, nombre: str, descripcion: str, fecha_vencimiento):
    """Modifica nombre, descripción y/o fecha límite. Vacío o None significa "no cambiar".
    Regla: la fecha límite no puede ser anterior a la fecha de creación. Retorna (exito, mensaje)."""
    tarjeta = buscar_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return False, 'No existe una tarjeta con ese Id.'

    cambios = []
    nombre = nombre.strip()
    if nombre and nombre != tarjeta.nombtarj:
        tarjeta.nombtarj = nombre
        cambios.append('nombre')
    descripcion = descripcion.strip()
    if descripcion and descripcion != tarjeta.descriptarj:
        tarjeta.descriptarj = descripcion
        cambios.append('descripción')
    if fecha_vencimiento and fecha_vencimiento != tarjeta.fecha_vencimiento:
        if tarjeta.fecha_creacion and fecha_vencimiento < tarjeta.fecha_creacion:
            return False, 'La fecha límite no puede ser anterior a la fecha de creación de la tarjeta.'
        tarjeta.fecha_vencimiento = fecha_vencimiento
        cambios.append('fecha límite')

    if not cambios:
        return False, 'No se ingresó ningún cambio.'
    if guardar_registro(tarjeta):
        return True, f'Tarjeta "{tarjeta.nombtarj}" actualizada ({", ".join(cambios)}).'
    return False, 'No se pudo modificar la tarjeta.'


def eliminar_tarjeta(id_tarjeta: int):
    """Borrado lógico: la tarjeta deja de verse y de contar en el reporte. Retorna (exito, mensaje)."""
    tarjeta = buscar_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return False, 'No existe una tarjeta con ese Id.'

    tarjeta.habilitado = 0
    if guardar_registro(tarjeta):
        return True, f'Tarjeta "{tarjeta.nombtarj}" eliminada.'
    return False, 'No se pudo eliminar la tarjeta.'


def mover_tarjeta(id_tarjeta: int, id_lista_destino: int):
    """Regla: solo se mueve entre listas del MISMO tablero. Retorna (exito, mensaje)."""
    tarjeta = buscar_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return False, 'No existe una tarjeta con ese Id.'
    destino = buscar_lista_por_id(id_lista_destino)
    if not destino:
        return False, 'No existe una lista con ese Id.'
    origen = tarjeta.id_lista
    if destino.id_lista == origen.id_lista:
        return False, 'La tarjeta ya está en esa lista.'
    if destino.id_tablero.id_tablero != origen.id_tablero.id_tablero:
        return False, 'Solo se puede mover a una lista del mismo tablero.'

    tarjeta.id_lista = destino
    tarjeta.posicion = siguiente_posicion_tarjeta(destino)
    if guardar_registro(tarjeta):
        return True, f'"{tarjeta.nombtarj}" movida de "{origen.nomblist}" a "{destino.nomblist}".'
    return False, 'No se pudo mover la tarjeta.'


def asignar_responsable(id_tarjeta: int, rut: str):
    """Regla: el responsable debe ser participante del proyecto. Retorna (exito, mensaje)."""
    tarjeta = buscar_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return False, 'No existe una tarjeta con ese Id.'
    if not validar_rut(rut):
        return False, 'El RUT no es válido.'
    proyecto = proyecto_de_tarjeta(tarjeta)
    participante = buscar_participante_por_rut(formatear_rut(rut), proyecto)
    if not participante:
        return False, f'Ese usuario no participa en el proyecto "{proyecto.nompro}".'
    if not participante.id_usuario.habilitado:
        return False, f'{participante.id_usuario.nombre} está deshabilitado y no puede recibir tarjetas.'

    tarjeta.id_responsable = participante
    if guardar_registro(tarjeta):
        return True, f'{participante.id_usuario.nombre} es ahora responsable de "{tarjeta.nombtarj}".'
    return False, 'No se pudo asignar el responsable.'


def cambiar_estado(id_tarjeta: int, estado: str):
    """Regla: solo se aceptan los estados definidos en la aplicación. Retorna (exito, mensaje)."""
    tarjeta = buscar_tarjeta_por_id(id_tarjeta)
    if not tarjeta:
        return False, 'No existe una tarjeta con ese Id.'
    if estado not in estados_tarjeta:
        return False, 'El estado no es válido.'
    if tarjeta.estado == estado:
        return False, f'La tarjeta ya está "{estado}".'

    tarjeta.estado = estado
    if guardar_registro(tarjeta):
        return True, f'"{tarjeta.nombtarj}" ahora está "{estado}".'
    return False, 'No se pudo cambiar el estado.' 