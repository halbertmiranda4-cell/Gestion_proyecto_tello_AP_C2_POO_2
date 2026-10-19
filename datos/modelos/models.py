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

database = conectar_db()


class BaseModel(Model):
    """Clase base para todos los modelos del proyecto."""
    class Meta:
        database = database


class Proyecto(BaseModel):
    id_proyecto = AutoField(column_name='ID_PROYECTO')
    nompro = CharField(column_name='NOMPRO', max_length=50)
    descripcion = CharField(column_name='DESCRIPCION', max_length=150, null=True)
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])

    class Meta:
        table_name = 'proyecto'


class Tablero(BaseModel):
    id_tablero = AutoField(column_name='ID_TABLERO')
    nomtab = CharField(column_name='NOMTAB', max_length=50)
    # unique=True: regla del enunciado, cada proyecto tiene un solo tablero
    id_proyecto = ForeignKeyField(column_name='ID_PROYECTO', model=Proyecto, field='id_proyecto', unique=True)
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])

    class Meta:
        table_name = 'tablero'


class Lista(BaseModel):
    id_lista = AutoField(column_name='ID_LISTA')
    nomblist = CharField(column_name='NOMBLIST', max_length=50)
    id_tablero = ForeignKeyField(column_name='ID_TABLERO', model=Tablero, field='id_tablero')
    posicion = IntegerField(column_name='POSICION')
    descriplist = CharField(column_name='DESCRIPLIST', max_length=150, null=True)

    class Meta:
        table_name = 'lista'


class Usuarios(BaseModel):
    id_usuario = AutoField(column_name='ID_USUARIO')
    nombre = CharField(column_name='NOMBRE', max_length=50)
    correo = CharField(column_name='CORREO', max_length=100, unique=True)
    contrasena = CharField(column_name='CONTRASENA', max_length=255)
    rut = CharField(column_name='RUT', max_length=12, unique=True)

    class Meta:
        table_name = 'usuarios'


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


class Tarjeta(BaseModel):
    id_tarjeta = AutoField(column_name='ID_TARJETA')
    nombtarj = CharField(column_name='NOMBTARJ', max_length=50)
    id_lista = ForeignKeyField(column_name='ID_LISTA', model=Lista, field='id_lista')
    descriptarj = CharField(column_name='DESCRIPTARJ', max_length=150, null=True)
    fecha_creacion = DateField(column_name='FECHA_CREACION', constraints=[SQL("DEFAULT curdate()")])
    fecha_vencimiento = DateField(column_name='FECHA_VENCIMIENTO', null=True)
    # Valores válidos: auxiliares.data_aplicacion.estados_tarjeta
    estado = CharField(column_name='ESTADO', max_length=20, constraints=[SQL("DEFAULT 'pendiente'")])
    posicion = IntegerField(column_name='POSICION')
    id_responsable = ForeignKeyField(column_name='ID_RESPONSABLE', model=UsuarioProyecto, field='id_usuario_proyecto', null=True)

    class Meta:
        table_name = 'tarjeta'


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

