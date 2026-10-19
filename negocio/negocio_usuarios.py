import bcrypt
from prettytable import PrettyTable
from datos.modelos.models import Usuarios
from datos.repositorios.repositorio_usuarios import (
    listado_usuarios,
    buscar_usuario_por_correo,
    buscar_usuario_por_rut,
    guardar_usuario
)
from auxiliares import validar_rut, formatear_rut, validar_correo

LARGO_MINIMO_CONTRASENA = 6


def lista_usuarios(tabla_usuarios: PrettyTable):
    usuarios = listado_usuarios()
    if usuarios:
        for usuario in usuarios:
            # La contraseña nunca se muestra
            tabla_usuarios.add_row([usuario.id_usuario, usuario.nombre, usuario.correo, usuario.rut])
    return tabla_usuarios


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

    if guardar_usuario(nuevo_usuario):
        return True, f'Usuario {nombre} registrado correctamente.'
    return False, 'No se pudo registrar el usuario.'