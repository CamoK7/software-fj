"""
Clase abstracta Entidad.

Representa cualquier "cosa" general del sistema (cliente, servicio, reserva).
No se puede crear un objeto de esta clase directamente, solo sirve de molde.
"""

from abc import ABC, abstractmethod  # ABC permite crear clases abstractas


class Entidad(ABC):
    """Clase abstracta base de todas las entidades del sistema."""

    def __init__(self, id_entidad):
        # Atributo "privado" (empieza con _) para proteger el identificador
        self._id = id_entidad

    @property
    def id(self):
        """Permite leer el identificador, pero no cambiarlo desde afuera."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase hija debe decir cómo se describe (método abstracto)."""
        pass
