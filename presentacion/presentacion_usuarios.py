from prettytable import PrettyTable
from negocio.negocio_usuarios import lista_usuarios, crear_usuario
from auxiliares import validar_rut, validar_correo

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


def mostrar_usuarios():
    tabla_usuarios = PrettyTable()
    tabla_usuarios.field_names = ['Id', 'Nombre', 'Correo', 'RUT']
    tabla_usuarios = lista_usuarios(tabla_usuarios)
    if tabla_usuarios.rows:
        print(tabla_usuarios)
    else:
        print('No hay usuarios registrados.\n')


def solicitar_datos_usuario():
    nombre = correo = rut = contrasena = ''

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
    while contrasena == '':
        contrasena = pedir_contrasena('Ingrese contraseña: ')
        confirmacion = pedir_contrasena('Repita la contraseña: ')
        if contrasena != confirmacion:
            print('Las contraseñas no coinciden. Intente nuevamente.')
            contrasena = ''

    exito, mensaje = crear_usuario(nombre, correo, rut, contrasena)
    print(('ERROR: ', 'OK: ')[exito] + mensaje + '\n')