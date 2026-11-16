from datetime import date
import bcrypt
from peewee import (
    Model,
    CharField,
    DateField,
    IntegerField,
    TextField,
    AutoField,
    ForeignKeyField,
    CompositeKey,
    SQL
)
from datos.conexion import conectar_db
from datos.modelos.dominio import crear_estado, crear_rol

database = conectar_db()


class BaseModel(Model):
    """Clase padre de todos los modelos (herencia): comparte la conexión a la base de datos."""
    class Meta:
        database = database


class BorradoLogico:
    """Clase de apoyo (mixin) que agrega el borrado lógico a los modelos que tienen el campo habilitado.
    La heredan Usuarios, Proyecto y ElementoTablero (y por lo tanto Lista y Tarjeta)."""

    @property
    def esta_habilitado(self) -> bool:
        return bool(self.habilitado)

    def deshabilitar(self):
        self.habilitado = 0

    def habilitar(self):
        self.habilitado = 1


class Proyecto(BorradoLogico, BaseModel):
    id_proyecto = AutoField(column_name='ID_PROYECTO')
    nompro = CharField(column_name='NOMPRO', max_length=50)
    descripcion = CharField(column_name='DESCRIPCION', max_length=150, null=True)
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])
    habilitado = IntegerField(column_name='HABILITADO', constraints=[SQL('DEFAULT 1')], default=1)

    class Meta:
        table_name = 'proyecto'

    def __str__(self):
        return self.nompro


class Tablero(BaseModel):
    id_tablero = AutoField(column_name='ID_TABLERO')
    nomtab = CharField(column_name='NOMTAB', max_length=50)
    # unique=True: regla del enunciado, cada proyecto tiene un solo tablero
    id_proyecto = ForeignKeyField(column_name='ID_PROYECTO', model=Proyecto, field='id_proyecto', unique=True)
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])

    class Meta:
        table_name = 'tablero'

    def __str__(self):
        return self.nomtab


class ElementoTablero(BorradoLogico, BaseModel):
    """Herencia de dominio: una Lista y una Tarjeta SON elementos de un tablero.
    Comparten los campos posicion y habilitado, y deben saber decir su nombre y su tipo.
    Polimorfismo: cada hija redefine nombre, tipo() y ubicacion()."""

    posicion = IntegerField(column_name='POSICION')
    habilitado = IntegerField(column_name='HABILITADO', constraints=[SQL('DEFAULT 1')], default=1)

    @property
    def nombre(self) -> str:
        raise NotImplementedError('Cada elemento debe definir su nombre')

    def tipo(self) -> str:
        raise NotImplementedError('Cada elemento debe definir su tipo')

    def ubicacion(self) -> str:
        raise NotImplementedError('Cada elemento debe definir dónde está')

    def resumen(self) -> str:
        """Igual para todos, pero usa los métodos que cada hija redefine."""
        return f'{self.tipo()} "{self.nombre}" (posición {self.posicion}) en {self.ubicacion()}'

    def __str__(self):
        return self.nombre


class Lista(ElementoTablero):
    id_lista = AutoField(column_name='ID_LISTA')
    nomblist = CharField(column_name='NOMBLIST', max_length=50)
    id_tablero = ForeignKeyField(column_name='ID_TABLERO', model=Tablero, field='id_tablero')
    descriplist = CharField(column_name='DESCRIPLIST', max_length=150, null=True)

    class Meta:
        table_name = 'lista'

    @property
    def nombre(self) -> str:
        return self.nomblist

    def tipo(self) -> str:
        return 'Lista'

    def ubicacion(self) -> str:
        return f'el tablero "{self.id_tablero}"'


class Usuarios(BorradoLogico, BaseModel):
    id_usuario = AutoField(column_name='ID_USUARIO')
    nombre = CharField(column_name='NOMBRE', max_length=50)
    correo = CharField(column_name='CORREO', max_length=100, unique=True)
    contrasena = CharField(column_name='CONTRASENA', max_length=255)
    rut = CharField(column_name='RUT', max_length=12, unique=True)
    habilitado = IntegerField(column_name='HABILITADO', constraints=[SQL('DEFAULT 1')], default=1)

    class Meta:
        table_name = 'usuarios'

    # Encapsulamiento: la contraseña solo se asigna y se compara mediante estos métodos,
    # así nunca queda guardada en texto plano.
    def establecer_contrasena(self, contrasena: str):
        self.contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_contrasena(self, contrasena: str) -> bool:
        return bcrypt.checkpw(contrasena.encode('utf-8'), self.contrasena.encode('utf-8'))

    def __str__(self):
        return f'{self.nombre} ({self.rut})'


class UsuarioProyecto(BaseModel):
    id_usuario_proyecto = AutoField(column_name='ID_USUARIO_PROYECTO')
    id_usuario = ForeignKeyField(column_name='ID_USUARIO', model=Usuarios, field='id_usuario')
    id_proyecto = ForeignKeyField(column_name='ID_PROYECTO', model=Proyecto, field='id_proyecto')
    rol = CharField(column_name='ROL', max_length=20)
    fecha_ingreso = DateField(column_name='FECHA_INGRESO', constraints=[SQL("DEFAULT curdate()")])

    class Meta:
        table_name = 'usuario_proyecto'
        indexes = (
            (('id_usuario', 'id_proyecto'), True),
        )

    @property
    def rol_actual(self):
        """Convierte el texto de la columna ROL en su objeto (Administrador o Miembro)."""
        return crear_rol(self.rol)

    def __str__(self):
        return f'{self.id_usuario.nombre} - {self.rol}'


class Tarjeta(ElementoTablero):
    id_tarjeta = AutoField(column_name='ID_TARJETA')
    nombtarj = CharField(column_name='NOMBTARJ', max_length=50)
    id_lista = ForeignKeyField(column_name='ID_LISTA', model=Lista, field='id_lista')
    descriptarj = CharField(column_name='DESCRIPTARJ', max_length=150, null=True)
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])
    fecha_vencimiento = DateField(column_name='FECHA_VENCIMIENTO', null=True)
    # Valores válidos: los estados definidos en datos/modelos/dominio.py
    estado = CharField(column_name='ESTADO', max_length=20, constraints=[SQL("DEFAULT 'pendiente'")])
    id_responsable = ForeignKeyField(column_name='ID_RESPONSABLE', model=UsuarioProyecto, field='id_usuario_proyecto', null=True)

    class Meta:
        table_name = 'tarjeta'

    @property
    def nombre(self) -> str:
        return self.nombtarj

    def tipo(self) -> str:
        return 'Tarjeta'

    def ubicacion(self) -> str:
        return f'la lista "{self.id_lista}"'

    @property
    def estado_actual(self):
        """Convierte el texto de la columna ESTADO en su objeto (Pendiente, EnProgreso o Completada)."""
        return crear_estado(self.estado)

    @property
    def proyecto(self):
        return self.id_lista.id_tablero.id_proyecto

    @property
    def nombre_responsable(self) -> str:
        if self.id_responsable is None:
            return 'Sin asignar'
        return self.id_responsable.id_usuario.nombre

    def esta_vencida(self) -> bool:
        # Polimorfismo: es el ESTADO el que decide si la tarjeta puede vencer
        return (self.fecha_vencimiento is not None
                and self.fecha_vencimiento < date.today()
                and self.estado_actual.puede_vencer())


class Comentario(BaseModel):
    id_comentario = AutoField(column_name='ID_COMENTARIO')
    texto = TextField(column_name='TEXTO')
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])
    id_usuario = ForeignKeyField(column_name='ID_USUARIO', model=Usuarios, field='id_usuario')
    id_tarjeta = ForeignKeyField(column_name='ID_TARJETA', model=Tarjeta, field='id_tarjeta')

    class Meta:
        table_name = 'comentario'


class Etiqueta(BaseModel):
    id_etiqueta = AutoField(column_name='ID_ETIQUETA')
    nometiq = CharField(column_name='NOMETIQ', max_length=30)
    color = CharField(column_name='COLOR', max_length=20)
    id_proyecto = ForeignKeyField(column_name='ID_PROYECTO', model=Proyecto, field='id_proyecto')

    class Meta:
        table_name = 'etiqueta'
        indexes = (
            (('id_proyecto', 'nometiq'), True),
        )


class TarjetaEtiqueta(BaseModel):
    id_tarjeta = ForeignKeyField(column_name='ID_TARJETA', model=Tarjeta, field='id_tarjeta')
    id_etiqueta = ForeignKeyField(column_name='ID_ETIQUETA', model=Etiqueta, field='id_etiqueta')

    class Meta:
        table_name = 'tarjeta_etiqueta'
        indexes = (
            (('id_tarjeta', 'id_etiqueta'), True),
        )
        primary_key = CompositeKey('id_tarjeta', 'id_etiqueta') 