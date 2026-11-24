"""
Clase Reserva.

Une un cliente, un servicio, una duración y un estado. Maneja la confirmación,
cancelación y procesamiento de la reserva, usando excepciones.

Estados posibles: pendiente, confirmada, cancelada, procesada, fallida
"""

import logging
from entidad import Entidad
from cliente import Cliente
from servicio import Servicio
from excepciones import (
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)


class Reserva(Entidad):
    """Reserva de un servicio hecha por un cliente."""

    def __init__(self, id_reserva, cliente, servicio, horas):
        # Se revisa que el cliente y el servicio sean objetos del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido")
        try:
            # El servicio revisa si la duración pedida es correcta para él
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as error:
            # Encadenamiento: se lanza un error de reserva pero se guarda la causa original
            raise ReservaInvalidaError(f"No se pudo crear la reserva: {error}") from error

        super().__init__(id_reserva)
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "pendiente"   # toda reserva nueva empieza pendiente
        self._costo = None           # se calcula al procesar

    @property
    def estado(self):
        """Estado actual de la reserva."""
        return self._estado

    @property
    def costo(self):
        """Costo final (solo tiene valor cuando la reserva fue procesada)."""
        return self._costo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    def confirmar(self):
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        try:
            if self._estado != "pendiente":
                raise OperacionNoPermitidaError(
                    f"La reserva {self._id} está '{self._estado}' y no se puede confirmar")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' no está disponible")
        except ServicioNoDisponibleError:
            # Si el servicio no está disponible, la reserva queda marcada como fallida
            self._estado = "fallida"
            raise  # se vuelve a lanzar el mismo error para que lo registre quien llamó
        else:
            # Solo se ejecuta si el try no lanzó ningún error
            self._estado = "confirmada"
            logging.info(f"Reserva {self._id} confirmada ({self._cliente.nombre} - {self._servicio.nombre})")

    def cancelar(self):
        """Cancela la reserva, salvo que ya esté cancelada o procesada."""
        if self._estado in ("cancelada", "procesada"):
            raise OperacionNoPermitidaError(
                f"La reserva {self._id} está '{self._estado}' y no se puede cancelar")
        self._estado = "cancelada"
        logging.info(f"Reserva {self._id} cancelada")

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Calcula el costo final y deja la reserva como procesada (debe estar confirmada)."""
        if self._estado != "confirmada":
            raise OperacionNoPermitidaError(
                f"La reserva {self._id} está '{self._estado}'; solo se procesan las confirmadas")
        try:
            costo = self._servicio.calcular_costo_total(self._horas, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Encadenamiento de excepciones: se explica el contexto y se guarda la causa
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva {self._id}") from error
        else:
            # Se ejecuta solo si el cálculo salió bien
            self._costo = costo
            self._estado = "procesada"
            logging.info(f"Reserva {self._id} procesada, costo final: ${costo:,.2f}")
            return costo
        finally:
            # Se ejecuta siempre, haya error o no
            logging.info(f"Fin del intento de procesar la reserva {self._id}")

    def describir(self):
        """Resumen de la reserva en una línea."""
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva {self._id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas} h | estado: {self._estado} | costo: {costo}")
