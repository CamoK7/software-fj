"""
Clase Cliente.

Guarda los datos personales de un cliente de Software FJ. Los atributos son
privados y solo se pueden cambiar a través de propiedades que validan el dato.
"""

from entidad import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):
    """Cliente de la empresa, con validaciones estrictas de sus datos."""

    def __init__(self, documento=None, nombre=None, correo=None, telefono=None):
        # Primero se valida el documento (es el identificador del cliente)
        self._validar_documento(documento)
        # Se llama al constructor de la clase padre guardando el documento como id
        super().__init__(documento)
        # Estas asignaciones usan los "setter" de abajo, que validan cada dato
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @staticmethod
    def _validar_documento(documento):
        """El documento es obligatorio, de 6 a 10 dígitos."""
        if documento is None:
            raise ClienteInvalidoError("El documento es obligatorio")
        if not isinstance(documento, str) or not documento.isdigit():
            raise ClienteInvalidoError("El documento debe contener solo números")
        if len(documento) < 6 or len(documento) > 10:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 10 dígitos")

    # ---------- nombre ----------
    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida y guarda el nombre."""
        if valor is None or not isinstance(valor, str) or valor.strip() == "":
            raise ClienteInvalidoError("El nombre es obligatorio")
        if len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 letras")
        # Se quitan los espacios para revisar que solo haya letras
        if not valor.replace(" ", "").isalpha():
            raise ClienteInvalidoError("El nombre solo puede tener letras y espacios")
        self._nombre = valor.strip()

    # ---------- correo ----------
    @property
    def correo(self):
        """Devuelve el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor):
        """Valida y guarda el correo (debe tener una @ y un punto después)."""
        if valor is None or not isinstance(valor, str) or valor.strip() == "":
            raise ClienteInvalidoError("El correo es obligatorio")
        partes = valor.split("@")  # separa el texto en la @
        if len(partes) != 2 or partes[0] == "" or "." not in partes[1]:
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido")
        self._correo = valor.strip()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Valida y guarda el teléfono (de 7 a 10 dígitos)."""
        if valor is None:
            raise ClienteInvalidoError("El teléfono es obligatorio")
        if not isinstance(valor, str) or not valor.isdigit():
            raise ClienteInvalidoError("El teléfono debe contener solo números")
        if len(valor) < 7 or len(valor) > 10:
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos")
        self._telefono = valor

    def describir(self):
        """Devuelve un texto con los datos del cliente (método de Entidad)."""
        return f"Cliente {self._nombre} (doc: {self._id}, correo: {self._correo}, tel: {self._telefono})"
