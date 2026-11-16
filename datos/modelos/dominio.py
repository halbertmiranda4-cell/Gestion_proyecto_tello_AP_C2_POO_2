from abc import ABC, abstractmethod


# ============================================================
#  ESTADOS DE UNA TARJETA
#  Herencia de dominio: Pendiente, EnProgreso y Completada SON un EstadoTarjeta.
#  Polimorfismo: cada estado responde distinto a los mismos métodos.
# ============================================================

class EstadoTarjeta(ABC):
    """Clase abstracta: define lo que todo estado de tarjeta debe saber responder."""

    nombre = ''   # texto que se guarda en la columna ESTADO de la base de datos

    @abstractmethod
    def simbolo(self) -> str:
        """Marca que se muestra en el tablero."""

    @abstractmethod
    def aporte_avance(self) -> float:
        """Cuánto aporta la tarjeta al avance del proyecto (0 a 1)."""

    def puede_vencer(self) -> bool:
        """Por defecto una tarjeta puede vencer. Completada lo redefine."""
        return True

    def etiqueta(self) -> str:
        return f'{self.simbolo()} {self.nombre}'

    def __str__(self) -> str:
        return self.nombre


class Pendiente(EstadoTarjeta):
    nombre = 'pendiente'

    def simbolo(self) -> str:
        return '[ ]'

    def aporte_avance(self) -> float:
        return 0.0


class EnProgreso(EstadoTarjeta):
    nombre = 'en progreso'

    def simbolo(self) -> str:
        return '[~]'

    def aporte_avance(self) -> float:
        return 0.5


class Completada(EstadoTarjeta):
    nombre = 'completada'

    def simbolo(self) -> str:
        return '[x]'

    def aporte_avance(self) -> float:
        return 1.0

    def puede_vencer(self) -> bool:
        return False   # una tarea terminada ya no se considera vencida


# ============================================================
#  ROLES DENTRO DE UN PROYECTO
#  Herencia de dominio: Administrador y Miembro SON un RolProyecto.
#  Polimorfismo: cada rol tiene permisos distintos.
# ============================================================

class RolProyecto(ABC):
    """Clase abstracta: define los permisos que todo rol debe declarar."""

    nombre = ''   # texto que se guarda en la columna ROL de la base de datos

    @abstractmethod
    def puede_gestionar_participantes(self) -> bool:
        """¿Puede agregar personas al proyecto?"""

    @abstractmethod
    def puede_eliminar_proyecto(self) -> bool:
        """¿Puede eliminar el proyecto?"""

    def permisos(self) -> str:
        """Resumen de permisos (se arma con los métodos que cada hijo redefine)."""
        lista = ['trabajar tarjetas']
        if self.puede_gestionar_participantes():
            lista.append('agregar participantes')
        if self.puede_eliminar_proyecto():
            lista.append('eliminar proyecto')
        return ', '.join(lista)

    def __str__(self) -> str:
        return self.nombre


class Administrador(RolProyecto):
    nombre = 'administrador'

    def puede_gestionar_participantes(self) -> bool:
        return True

    def puede_eliminar_proyecto(self) -> bool:
        return True


class Miembro(RolProyecto):
    nombre = 'miembro'

    def puede_gestionar_participantes(self) -> bool:
        return False

    def puede_eliminar_proyecto(self) -> bool:
        return False


# ============================================================
#  "Fábricas": convierten el texto guardado en la base de datos en el objeto correcto
# ============================================================

ESTADOS = {estado.nombre: estado for estado in (Pendiente(), EnProgreso(), Completada())}
ROLES = {rol.nombre: rol for rol in (Administrador(), Miembro())}


def crear_estado(nombre: str) -> EstadoTarjeta:
    return ESTADOS.get(nombre, ESTADOS['pendiente'])


def crear_rol(nombre: str) -> RolProyecto:
    return ROLES.get(nombre, ROLES['miembro']) 