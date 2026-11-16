from prettytable import PrettyTable
from negocio.negocio_usuarios import ServicioUsuarios
from presentacion.presentacion_comun import mostrar_resultado, solicitar_eliminacion
from auxiliares import validar_rut, validar_correo, validar_contrasena, pedir_texto, pedir_entero, confirmar

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


servicio_usuarios = ServicioUsuarios()   # objeto de la capa de negocio


def mostrar_usuarios(habilitados: bool = True) -> bool:
    """Muestra los usuarios habilitados (o los eliminados si habilitados=False).
    Retorna False si no hay ninguno que mostrar."""
    usuarios = servicio_usuarios.listar(habilitados)
    if not usuarios:
        print('No hay usuarios ' + ('registrados.' if habilitados else 'deshabilitados.') + '\n')
        return False

    tabla_usuarios = PrettyTable()
    tabla_usuarios.field_names = ['Id', 'Nombre', 'Correo', 'RUT']
    for usuario in usuarios:
        tabla_usuarios.add_row([usuario.id_usuario, usuario.nombre, usuario.correo, usuario.rut])
    if not habilitados:
        print('\nUsuarios deshabilitados:')
    print(tabla_usuarios)
    return True


def pedir_contrasena_confirmada() -> str:
    """Pide una contraseña segura y que se repita igual. Muestra todos los errores de una vez."""
    print('La contraseña debe tener 8 caracteres o más, mayúscula, minúscula, número y un símbolo (@ $ # ! * &).')
    while True:
        contrasena = pedir_contrasena('Ingrese contraseña: ')
        errores = validar_contrasena(contrasena)
        if errores:
            print('Contraseña inválida, revise los siguientes errores:')
            for error in errores:
                print(f'  - {error}')
            continue
        if contrasena == pedir_contrasena('Repita la contraseña: '):
            return contrasena
        print('Las contraseñas no coinciden. Intente nuevamente.')


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

    mostrar_resultado(*servicio_usuarios.crear(nombre, correo, rut, contrasena))


def solicitar_modificacion_usuario():
    mostrar_usuarios()
    usuario = servicio_usuarios.obtener(pedir_entero('Id del usuario a modificar: '))
    if not usuario:
        print('ERROR: No existe un usuario con ese Id.\n')
        return

    print('Deje en blanco (Enter) lo que no quiera cambiar. El RUT no se puede modificar.')
    nombre = pedir_texto(f'Nombre [{usuario.nombre}]: ', obligatorio=False, largo_maximo=50)
    correo = pedir_texto(f'Correo [{usuario.correo}]: ', obligatorio=False, largo_maximo=100)
    contrasena = ''
    if confirmar('¿Desea cambiar la contraseña?'):
        contrasena = pedir_contrasena_confirmada()

    mostrar_resultado(*servicio_usuarios.modificar(usuario.id_usuario, nombre, correo, contrasena))


def solicitar_deshabilitar_usuario():
    if not mostrar_usuarios():
        return
    id_usuario = pedir_entero('Id del usuario a eliminar: ')
    solicitar_eliminacion(servicio_usuarios, id_usuario,
                          'El usuario quedará deshabilitado: no podrá participar en proyectos ni recibir tarjetas. ¿Continuar?')


def solicitar_habilitar_usuario():
    if not mostrar_usuarios(habilitados=False):
        return
    id_usuario = pedir_entero('Id del usuario a habilitar: ')
    mostrar_resultado(*servicio_usuarios.habilitar(id_usuario)) 