import bcrypt
from prettytable import PrettyTable
from datos.modelos.models import Usuarios
from datos.repositorios.repositorio_base import guardar_registro
from datos.repositorios.repositorio_usuarios import (
    listado_usuarios,
    buscar_usuario_por_id,
    buscar_usuario_por_correo,
    buscar_usuario_por_rut,
    guardar_usuario
)
from auxiliares import validar_rut, formatear_rut, validar_correo

LARGO_MINIMO_CONTRASENA = 6


def lista_usuarios(tabla_usuarios: PrettyTable, habilitados: bool = True):
    usuarios = listado_usuarios(habilitados)
    if usuarios:
        for usuario in usuarios:
            # La contraseña nunca se muestra
            tabla_usuarios.add_row([usuario.id_usuario, usuario.nombre, usuario.correo, usuario.rut])
    return tabla_usuarios


def obtener_usuario(id_usuario: int):
    return buscar_usuario_por_id(id_usuario)


def encriptar_contrasena(contrasena: str) -> str:
    return bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verificar_contrasena(contrasena: str, contrasena_encriptada: str) -> bool:
    return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_encriptada.encode('utf-8'))


def crear_usuario(nombre: str, correo: str, rut: str, contrasena: str):
    """Aplica las reglas de negocio y, si todo está bien, guarda el usuario.
    Retorna (exito, mensaje) para que la capa de presentación muestre el resultado."""
    nombre = nombre.strip()
    correo = correo.strip().lower()

    # Reglas de negocio
    if not nombre:
        return False, 'El nombre es obligatorio.'
    if not validar_correo(correo):
        return False, 'El correo no tiene un formato válido.'
    if not validar_rut(rut):
        return False, 'El RUT no es válido.'
    if len(contrasena) < LARGO_MINIMO_CONTRASENA:
        return False, f'La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres.'

    rut = formatear_rut(rut)
    if buscar_usuario_por_correo(correo):
        return False, 'Ya existe un usuario con ese correo.'
    if buscar_usuario_por_rut(rut):
        return False, 'Ya existe un usuario con ese RUT.'

    nuevo_usuario = Usuarios()
    nuevo_usuario.nombre = nombre
    nuevo_usuario.correo = correo
    nuevo_usuario.rut = rut
    nuevo_usuario.contrasena = encriptar_contrasena(contrasena)
    nuevo_usuario.habilitado = 1

    if guardar_usuario(nuevo_usuario):
        return True, f'Usuario {nombre} registrado correctamente.'
    return False, 'No se pudo registrar el usuario.'


def modificar_usuario(id_usuario: int, nombre: str, correo: str, contrasena: str):
    """Modifica nombre, correo y/o contraseña. Un campo vacío significa "no cambiar".
    El RUT no se modifica porque identifica a la persona. Retorna (exito, mensaje)."""
    usuario = buscar_usuario_por_id(id_usuario)
    if not usuario:
        return False, 'No existe un usuario con ese Id.'
    if not usuario.habilitado:
        return False, 'El usuario está deshabilitado. Habilítelo antes de modificarlo.'

    cambios = []

    nombre = nombre.strip()
    if nombre and nombre != usuario.nombre:
        usuario.nombre = nombre
        cambios.append('nombre')

    correo = correo.strip().lower()
    if correo and correo != usuario.correo:
        if not validar_correo(correo):
            return False, 'El correo no tiene un formato válido.'
        otro = buscar_usuario_por_correo(correo)
        if otro and otro.id_usuario != usuario.id_usuario:
            return False, 'Ya existe otro usuario con ese correo.'
        usuario.correo = correo
        cambios.append('correo')

    if contrasena:
        if len(contrasena) < LARGO_MINIMO_CONTRASENA:
            return False, f'La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres.'
        usuario.contrasena = encriptar_contrasena(contrasena)
        cambios.append('contraseña')

    if not cambios:
        return False, 'No se ingresó ningún cambio.'
    if guardar_registro(usuario):
        return True, f'Usuario {usuario.nombre} actualizado ({", ".join(cambios)}).'
    return False, 'No se pudo modificar el usuario.'


def cambiar_habilitado(id_usuario: int, habilitar: bool):
    """Borrado lógico: deshabilita o vuelve a habilitar un usuario sin borrar sus datos.
    Retorna (exito, mensaje)."""
    usuario = buscar_usuario_por_id(id_usuario)
    if not usuario:
        return False, 'No existe un usuario con ese Id.'
    estado = 'habilitado' if habilitar else 'deshabilitado'
    if bool(usuario.habilitado) == habilitar:
        return False, f'{usuario.nombre} ya está {estado}.'

    usuario.habilitado = int(habilitar)
    if guardar_registro(usuario):
        return True, f'{usuario.nombre} quedó {estado}.'
    return False, 'No se pudo cambiar el estado del usuario.' 