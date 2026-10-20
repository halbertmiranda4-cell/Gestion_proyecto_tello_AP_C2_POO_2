from prettytable import PrettyTable
from negocio.negocio_usuarios import (
    lista_usuarios,
    crear_usuario,
    obtener_usuario,
    modificar_usuario,
    cambiar_habilitado
)
from auxiliares import validar_rut, validar_correo, pedir_texto, pedir_entero, confirmar, operacion_cancelada

try:
    # maskpass muestra asteriscos mientras se escribe la contraseña
    from maskpass import askpass

    def pedir_contrasena(mensaje):
        return askpass(prompt=mensaje, mask='*')
except ImportError:
    # Si maskpass no está instalado, se usa getpass (no muestra nada al escribir)
    from getpass import getpass

    def pedir_contrasena(mensaje):
        return getpass(mensaje)


def mostrar_resultado(exito: bool, mensaje: str):
    print(('ERROR: ', 'OK: ')[exito] + mensaje + '\n')


def mostrar_usuarios(habilitados: bool = True) -> bool:
    """Muestra los usuarios habilitados (o los eliminados si habilitados=False).
    Retorna False si no hay ninguno que mostrar."""
    tabla_usuarios = PrettyTable()
    tabla_usuarios.field_names = ['Id', 'Nombre', 'Correo', 'RUT']
    tabla_usuarios = lista_usuarios(tabla_usuarios, habilitados)
    if tabla_usuarios.rows:
        if not habilitados:
            print('\nUsuarios deshabilitados:')
        print(tabla_usuarios)
        return True
    print('No hay usuarios ' + ('registrados.' if habilitados else 'deshabilitados.') + '\n')
    return False


def pedir_contrasena_confirmada() -> str:
    while True:
        contrasena = pedir_contrasena('Ingrese contraseña: ')
        confirmacion = pedir_contrasena('Repita la contraseña: ')
        if contrasena and contrasena == confirmacion:
            return contrasena
        print('Las contraseñas no coinciden o están vacías. Intente nuevamente.')


def solicitar_datos_usuario():
    nombre = correo = rut = ''

    while nombre == '':
        nombre = input('Ingrese nombre: ').strip()
    while correo == '':
        correo = input('Ingrese correo: ').strip()
        if correo and not validar_correo(correo):
            print('Correo inválido. Intente nuevamente.')
            correo = ''
    while rut == '':
        rut = input('Ingrese RUT (ej: 12.345.678-5): ').strip()
        if rut and not validar_rut(rut):
            print('RUT inválido. Intente nuevamente.')
            rut = ''
    contrasena = pedir_contrasena_confirmada()

    mostrar_resultado(*crear_usuario(nombre, correo, rut, contrasena))


def solicitar_modificacion_usuario():
    mostrar_usuarios()
    usuario = obtener_usuario(pedir_entero('Id del usuario a modificar: '))
    if not usuario:
        print('ERROR: No existe un usuario con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar. El RUT no se puede modificar.')
    nombre = pedir_texto(f'Nombre [{usuario.nombre}]: ', obligatorio=False, largo_maximo=50)
    correo = pedir_texto(f'Correo [{usuario.correo}]: ', obligatorio=False, largo_maximo=100)
    contrasena = ''
    if confirmar('¿Desea cambiar la contraseña?'):
        contrasena = pedir_contrasena_confirmada()

    mostrar_resultado(*modificar_usuario(usuario.id_usuario, nombre, correo, contrasena))


def solicitar_deshabilitar_usuario():
    if not mostrar_usuarios():
        return
    id_usuario = pedir_entero('Id del usuario a eliminar: ')
    if confirmar('El usuario quedará deshabilitado: no podrá participar en proyectos ni recibir tarjetas. ¿Continuar?'):
        mostrar_resultado(*cambiar_habilitado(id_usuario, False))
    else:
        print(operacion_cancelada)


def solicitar_habilitar_usuario():
    if not mostrar_usuarios(habilitados=False):
        return
    id_usuario = pedir_entero('Id del usuario a habilitar: ')
    mostrar_resultado(*cambiar_habilitado(id_usuario, True)) 