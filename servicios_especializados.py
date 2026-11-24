"""
Servicios especializados de Software FJ.

Hay tres tipos, todos heredan de la clase abstracta Servicio:
  - ReservaSala
  - AlquilerEquipo
  - Asesoria
Cada uno sobrescribe validar_parametros, calcular_costo y describir (polimorfismo).
"""

from servicio import Servicio
from excepciones import ServicioInvalidoError


class ReservaSala(Servicio):
    """Reserva de una sala de reuniones por horas."""

    def __init__(self, id_servicio=None, nombre=None, precio_hora=None, capacidad=None):
        super().__init__(id_servicio, nombre, precio_hora)  # datos comunes
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero mayor que cero")
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        """Una sala se puede reservar de 1 a 8 horas."""
        self._validar_horas(horas, 8)

    def calcular_costo(self, horas):
        """Costo de la sala = precio por hora x horas."""
        return self._precio_hora * horas

    def describir(self):
        return f"Sala '{self._nombre}' para {self._capacidad} personas, ${self._precio_hora:,.0f} por hora"


class AlquilerEquipo(Servicio):
    """Alquiler de un equipo (portátil, proyector, etc.) con un depósito fijo."""

    def __init__(self, id_servicio=None, nombre=None, precio_hora=None, tipo_equipo=None, deposito=50000):
        super().__init__(id_servicio, nombre, precio_hora)
        if tipo_equipo is None or not isinstance(tipo_equipo, str) or tipo_equipo.strip() == "":
            raise ServicioInvalidoError("Debe indicar el tipo de equipo")
        if isinstance(deposito, bool) or not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError("El depósito debe ser un número mayor o igual a cero")
        self._tipo_equipo = tipo_equipo.strip()
        self._deposito = deposito

    def validar_parametros(self, horas):
        """Un equipo se puede alquilar de 1 a 24 horas."""
        self._validar_horas(horas, 24)

    def calcular_costo(self, horas):
        """Costo del equipo = precio por hora x horas + depósito."""
        return self._precio_hora * horas + self._deposito

    def describir(self):
        return (f"Alquiler de {self._tipo_equipo} '{self._nombre}', "
                f"${self._precio_hora:,.0f} por hora + ${self._deposito:,.0f} de depósito")


class Asesoria(Servicio):
    """Asesoría con un especialista. Si es senior tiene un recargo del 20 %."""

    def __init__(self, id_servicio=None, nombre=None, precio_hora=None, especialista=None, nivel="junior"):
        super().__init__(id_servicio, nombre, precio_hora)
        if especialista is None or not isinstance(especialista, str) or especialista.strip() == "":
            raise ServicioInvalidoError("Debe indicar el nombre del especialista")
        if nivel not in ("junior", "senior"):
            raise ServicioInvalidoError(f"El nivel '{nivel}' no es válido (use 'junior' o 'senior')")
        self._especialista = especialista.strip()
        self._nivel = nivel

    def validar_parametros(self, horas):
        """Una asesoría dura de 1 a 4 horas."""
        self._validar_horas(horas, 4)

    def calcular_costo(self, horas):
        """Costo = precio por hora x horas (+20 % si el especialista es senior)."""
        costo = self._precio_hora * horas
        if self._nivel == "senior":
            costo = costo * 1.20
        return costo

    def describir(self):
        return (f"Asesoría '{self._nombre}' con {self._especialista} (nivel {self._nivel}), "
                f"${self._precio_hora:,.0f} por hora")
