from datos.modelos.models import Usuarios
from datos.repositorios.repositorio_usuarios import RepositorioUsuarios
from negocio.servicio_base import ServicioBase
from auxiliares import Rut, validar_correo, validar_contrasena


class ServicioUsuarios(ServicioBase):
    """Reglas de negocio de los usuarios."""

    def __init__(self):
        super().__init__(RepositorioUsuarios())

    def listar(self, habilitados: bool = True):
        return self._repositorio.listar_por_estado(habilitados)

    def crear(self, nombre: str, correo: str, rut: str, contrasena: str):
        """Valida los datos y registra el usuario. Retorna (exito, mensaje)."""
        nombre = nombre.strip()
        correo = correo.strip().lower()
        rut = Rut(rut)

        if not nombre:
            return False, 'El nombre es obligatorio.'
        if not validar_correo(correo):
            return False, 'El correo no tiene un formato válido.'
        if not rut.es_valido():
            return False, 'El RUT no es válido.'
        errores = validar_contrasena(contrasena)
        if errores:
            return False, 'Contraseña insegura. ' + ' '.join(errores)
        if self._repositorio.buscar_por_correo(correo):
            return False, 'Ya existe un usuario con ese correo.'
        if self._repositorio.buscar_por_rut(rut.formateado()):
            return False, 'Ya existe un usuario con ese RUT.'

        usuario = Usuarios(nombre=nombre, correo=correo, rut=rut.formateado(), habilitado=1)
        usuario.establecer_contrasena(contrasena)
        if self._repositorio.guardar(usuario):
            return True, f'Usuario {usuario} registrado correctamente (Id {usuario.id_usuario}).'
        return False, 'No se pudo registrar el usuario.'

    def modificar(self, id_usuario: int, nombre: str, correo: str, contrasena: str):
        """Modifica nombre, correo y/o contraseña. Vacío = no cambiar. El RUT no se modifica."""
        usuario = self.obtener(id_usuario)
        if not usuario:
            return False, 'No existe un usuario con ese Id.'
        if not usuario.esta_habilitado:
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
            otro = self._repositorio.buscar_por_correo(correo)
            if otro and otro.id_usuario != usuario.id_usuario:
                return False, 'Ya existe otro usuario con ese correo.'
            usuario.correo = correo
            cambios.append('correo')

        if contrasena:
            errores = validar_contrasena(contrasena)
            if errores:
                return False, 'Contraseña insegura. ' + ' '.join(errores)
            usuario.establecer_contrasena(contrasena)
            cambios.append('contraseña')

        if not cambios:
            return False, 'No se ingresó ningún cambio.'
        if self._repositorio.guardar(usuario):
            return True, f'Usuario {usuario.nombre} actualizado ({", ".join(cambios)}).'
        return False, 'No se pudo modificar el usuario.'

    def iniciar_sesion(self, correo: str, contrasena: str):
        """Comprueba correo y contraseña. Retorna (exito, mensaje, usuario)."""
        correo = correo.strip().lower()
        if not validar_correo(correo):
            return False, 'El correo no tiene un formato válido.', None
        usuario = self._repositorio.buscar_por_correo(correo)
        # Mismo mensaje si no existe el correo o si la contraseña está mal:
        # así no se revela qué correos están registrados.
        if not usuario or not self.__contrasena_correcta(usuario, contrasena):
            return False, 'Correo o contraseña incorrectos.', None
        if not usuario.esta_habilitado:
            return False, f'{usuario.nombre} está deshabilitado y no puede iniciar sesión.', None
        return True, f'Bienvenido/a, {usuario.nombre}.', usuario

    @staticmethod
    def __contrasena_correcta(usuario, contrasena: str) -> bool:
        """Los usuarios de prueba cargados por SQL no tienen contraseña encriptada:
        bcrypt lanza ValueError con ellos, y eso se considera contraseña incorrecta."""
        try:
            return usuario.verificar_contrasena(contrasena)
        except ValueError:
            return False

    def eliminar(self, id_usuario: int):
        """Polimorfismo: en Usuarios, eliminar = deshabilitar (borrado lógico)."""
        return self.__cambiar_estado(id_usuario, habilitar=False)

    def habilitar(self, id_usuario: int):
        return self.__cambiar_estado(id_usuario, habilitar=True)

    def __cambiar_estado(self, id_usuario: int, habilitar: bool):
        """Método privado: solo lo usan eliminar() y habilitar() de esta clase."""
        usuario = self.obtener(id_usuario)
        if not usuario:
            return False, 'No existe un usuario con ese Id.'
        estado = 'habilitado' if habilitar else 'deshabilitado'
        if usuario.esta_habilitado == habilitar:
            return False, f'{usuario.nombre} ya está {estado}.'
        usuario.habilitar() if habilitar else usuario.deshabilitar()
        if self._repositorio.guardar(usuario):
            return True, f'{usuario.nombre} quedó {estado}.'
        return False, 'No se pudo cambiar el estado del usuario.' 